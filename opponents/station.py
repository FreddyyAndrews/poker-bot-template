"""station: a calling station. Never raises, never folds."""


def decide(state):
    return {"action": "check" if state["can_check"] else "call"}
