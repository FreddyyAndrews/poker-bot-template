"""aggressive: plays most hands and bets whenever it can; bluffs a lot."""
import random


def decide(state):
    # seed by the deal, not the match id, so duplicate comparisons replay identically
    rng = random.Random(f"{state['hand_num']}:{state['your_cards']}:{len(state['action_log'])}")
    legal, pot = state["legal_actions"], state["pot"]
    if legal["can_raise"] and (state["can_check"] or rng.random() < 0.35):
        size = state["current_bet"] + max(state["big_blind"], int(pot * rng.choice([0.5, 0.75, 1.0])))
        return {"action": "raise", "amount": min(legal["max_raise_to"], max(legal["min_raise_to"], size))}
    if state["can_check"]:
        return {"action": "check"}
    return {"action": "call"} if rng.random() < 0.8 else {"action": "fold"}
