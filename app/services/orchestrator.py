from app.agents.communication_agent import run_communication_agent
from app.agents.decision_agent import run_decision_agent
from app.agents.fraud_agent import run_fraud_agent
from app.agents.intake_agent import run_intake_agent
from app.agents.payout_agent import run_payout_agent
from app.memory.state_store import save_state
from app.schemas.state_schema import ClaimState
from app.services.missing_info_service import build_missing_info_response
from app.services.timing import measure_latency_ms
from app.services.workflow_event_service import log_workflow_event


def run_agent_with_logging(
    state: ClaimState,
    agent_name: str,
    agent_function,
) -> ClaimState:
    claim_id = state.claim.get("claim_id")

    log_workflow_event(
        claim_id=claim_id,
        event_type="AGENT_STARTED",
        agent_name=agent_name,
        status="STARTED",
    )

    try:
        new_state, latency_ms = measure_latency_ms(
            lambda: agent_function(state)
        )

        log_workflow_event(
            claim_id=claim_id,
            event_type="AGENT_COMPLETED",
            agent_name=agent_name,
            status="SUCCESS",
            latency_ms=latency_ms,
            payload_json={
                "status": new_state.status,
            },
        )

        return new_state

    except Exception as error:
        log_workflow_event(
            claim_id=claim_id,
            event_type="AGENT_FAILED",
            agent_name=agent_name,
            status="FAILED",
            payload_json={
                "error": str(error),
            },
        )

        raise


def run_workflow_from_state(state: ClaimState) -> dict:
    claim_id = state.claim.get("claim_id")

    log_workflow_event(
        claim_id=claim_id,
        event_type="WORKFLOW_STARTED",
        status="STARTED",
        payload_json={
            "initial_status": state.status,
        },
    )

    state.audit_trail.append("Workflow execution started")

    state = run_agent_with_logging(
        state=state,
        agent_name="intake_agent",
        agent_function=run_intake_agent,
    )

    if state.status == "MISSING_INFORMATION":
        state.audit_trail.append(
            "Workflow paused because claim information is missing"
        )

        log_workflow_event(
            claim_id=claim_id,
            event_type="WORKFLOW_PAUSED",
            status="PAUSED",
            payload_json={
                "reason": "missing_information",
                "missing_fields": state.intake_agent_result.get("missing_fields", []),
            },
        )

        state = run_agent_with_logging(
            state=state,
            agent_name="communication_agent",
            agent_function=run_communication_agent,
        )

        save_state(state)

        return build_missing_info_response(state)

    if state.status == "INTAKE_FAILED":
        state.audit_trail.append(
            "Workflow stopped because intake failed"
        )

        log_workflow_event(
            claim_id=claim_id,
            event_type="WORKFLOW_FAILED",
            status="FAILED",
            payload_json={
                "reason": "intake_failed",
                "errors": state.errors,
            },
        )

        state = run_agent_with_logging(
            state=state,
            agent_name="communication_agent",
            agent_function=run_communication_agent,
        )

        save_state(state)

        return {
            "status": state.status,
            "message": "Claim intake failed after maximum retries.",
            "claim": state.claim,
            "errors": state.errors,
            "communication_result": state.communication_result,
            "audit_trail": state.audit_trail,
        }

    state = run_agent_with_logging(
        state=state,
        agent_name="fraud_agent",
        agent_function=run_fraud_agent,
    )

    state = run_agent_with_logging(
        state=state,
        agent_name="payout_agent",
        agent_function=run_payout_agent,
    )

    state = run_agent_with_logging(
        state=state,
        agent_name="decision_agent",
        agent_function=run_decision_agent,
    )

    log_workflow_event(
        claim_id=claim_id,
        event_type="DECISION_MADE",
        status=state.status,
        agent_name="decision_agent",
        payload_json={
            "decision_result": state.decision_result,
        },
    )

    state = run_agent_with_logging(
        state=state,
        agent_name="communication_agent",
        agent_function=run_communication_agent,
    )

    state.audit_trail.append("Claim workflow completed")

    log_workflow_event(
        claim_id=claim_id,
        event_type="WORKFLOW_COMPLETED",
        status=state.status,
        payload_json={
            "final_status": state.status,
            "decision_result": state.decision_result,
        },
    )

    save_state(state)

    return state.model_dump()


def process_new_claim(claim: dict) -> dict:
    state = ClaimState(claim=claim)

    state.audit_trail.append("New claim received")

    save_state(state)

    log_workflow_event(
        claim_id=claim.get("claim_id"),
        event_type="CLAIM_RECEIVED",
        status="SUCCESS",
        payload_json={
            "claim": claim,
        },
    )

    return run_workflow_from_state(state)