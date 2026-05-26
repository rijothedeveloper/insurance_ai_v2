from typing import Any, Callable, Dict, Tuple

from app.schemas.state_schema import ClaimState
from app.services.workflow_event_service import log_workflow_event
from app.tools.tool_audit import record_tool_call


def call_tool_with_retries(
    state: ClaimState,
    tool_name: str,
    tool_input: Dict[str, Any],
    tool_function: Callable[..., Dict[str, Any]],
    retry_key: str,
) -> Tuple[ClaimState, Dict[str, Any]]:
    max_retries = state.max_retries[retry_key]

    last_error = None

    for attempt in range(1, max_retries + 1):
        try:
            output = tool_function(**tool_input)

            state = record_tool_call(
                state=state,
                tool_name=tool_name,
                tool_input=tool_input,
                tool_output=output,
                status="SUCCESS",
            )

            state.confidence_scores[tool_name] = output.get(
                "confidence",
                1.0,
            )

            return state, output

        except Exception as error:
            last_error = error
            state.retry_counts[retry_key] += 1

            log_workflow_event(
                claim_id=state.claim.get("claim_id"),
                event_type="RETRY_OCCURRED",
                tool_name=tool_name,
                status="FAILED",
                payload_json={
                    "attempt": attempt,
                    "max_retries": max_retries,
                    "error": str(error),
                },
            )

            state = record_tool_call(
                state=state,
                tool_name=tool_name,
                tool_input=tool_input,
                tool_output=None,
                status="FAILED",
                error=str(error),
            )

            state.audit_trail.append(
                f"{tool_name} attempt {attempt} failed"
            )

    raise RuntimeError(
        f"{tool_name} failed after {max_retries} retries: {last_error}"
    )