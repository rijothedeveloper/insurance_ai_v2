from typing import Dict, Any


def lookup_policy(customer_id: str) -> Dict[str, Any]:
    """
    Mock Policy Lookup Tool.

    Later this can call a real endpoint:
    GET /policy/{customer_id}
    """

    mock_policies = {
        "CUS-921": {
            "policy_active": True,
            "coverage_limit": 10000,
            "deductible": 500,
            "policy_type": "Auto",
        },
        "CUS-100": {
            "policy_active": True,
            "coverage_limit": 5000,
            "deductible": 1000,
            "policy_type": "Auto",
        },
        "CUS-999": {
            "policy_active": False,
            "coverage_limit": 0,
            "deductible": 0,
            "policy_type": "Auto",
        },
    }

    default_policy = {
        "policy_active": True,
        "coverage_limit": 7500,
        "deductible": 750,
        "policy_type": "Auto",
    }

    return mock_policies.get(customer_id, default_policy)