"""chaos: a random legal action every time (reproducible per hand)."""
import random


def decide(state):
    # seed by the deal, not the match id, so duplicate comparisons replay identically
    rng = random.Random(f"{state['hand_num']}:{state['your_cards']}:{len(state['action_log'])}")
    legal = state["legal_actions"]
    options = [{"action": "fold"}, {"action": "check" if state["can_check"] else "call"}]
    if legal["can_raise"]:
        options.append({"action": "raise",
                        "amount": rng.randint(legal["min_raise_to"], legal["max_raise_to"])})
    return rng.choice(options)
