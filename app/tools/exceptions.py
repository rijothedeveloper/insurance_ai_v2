class ToolError(Exception):
    """Base error for tool failures."""


class FraudToolError(ToolError):
    """Raised when the fraud tool fails."""