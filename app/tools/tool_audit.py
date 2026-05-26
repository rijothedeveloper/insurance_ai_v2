from typing import Any, Dict, Optional

from app.schemas.state_schema import ClaimState


def record_tool_call(
    state: ClaimState,
    tool_name: str,
    tool_input: Dict[str, Any],
    tool_output: Optional[Dict[str, Any]] = None,
    status: str = "SUCCESS",
    error: Optional[str] = None,
) -> ClaimState:
    audit_record = {
        "tool_name": tool_name,
        "status": status,
        "input": tool_input,
        "output": tool_output,
        "error": error,
    }

    state.tool_audit_trail.append(audit_record)

    if tool_output is not None:
        state.tool_results[tool_name] = tool_output

    if status == "SUCCESS":
        state.audit_trail.append(
            f"Tool called: {tool_name} with status SUCCESS"
        )
    else:
        state.audit_trail.append(
            f"Tool called: {tool_name} with status {status}: {error}"
        )

    return state