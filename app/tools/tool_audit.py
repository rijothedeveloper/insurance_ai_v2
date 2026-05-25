from typing import Any, Dict

from app.schemas.state_schema import ClaimState


def record_tool_call(
    state: ClaimState,
    tool_name: str,
    tool_input: Dict[str, Any],
    tool_output: Dict[str, Any],
    status: str = "SUCCESS",
) -> ClaimState:
    state.tool_results[tool_name] = tool_output

    state.tool_audit_trail.append(
        {
            "tool_name": tool_name,
            "status": status,
            "input": tool_input,
            "output": tool_output,
        }
    )

    state.audit_trail.append(
        f"Tool called: {tool_name} with status {status}"
    )

    return state