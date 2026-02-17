from fastapi import HTTPException

VALID_TRANSITIONS = {
    "pending": ["assigned", "cancelled"],
    "assigned": ["in_progress", "cancelled"],
    "in_progress": ["delivered"],
}

def validate_status_transition(current_status: str, new_status: str):
    allowed = VALID_TRANSITIONS.get(current_status, [])
    
    if new_status not in allowed:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid transition: {current_status} → {new_status}"
        )