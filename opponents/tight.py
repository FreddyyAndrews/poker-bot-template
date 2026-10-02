"""tight: plays few hands, bets only with a made hand, folds to pressure."""
import eval7

PREMIUM = {"AA", "KK", "QQ", "JJ", "TT", "99", "AK", "AQ", "AJ", "KQ"}
RANKS = "23456789TJQKA"


def hand_class(cards):
    r = sorted((c[0] for c in cards), key=RANKS.index, reverse=True)
    return "".join(r)


def made_hand(state):
    cards = [eval7.Card(c) for c in state["your_cards"] + state["community_cards"]]
    return eval7.handtype(eval7.evaluate(cards))


def decide(state):
    legal, owed, pot = state["legal_actions"], state["amount_owed"], state["pot"]
    if state["street"] == "preflop":
        if hand_class(state["your_cards"]) in PREMIUM:
            if legal["can_raise"]:
                return {"action": "raise", "amount": min(legal["max_raise_to"],
                                                         max(legal["min_raise_to"], 3 * state["big_blind"]))}
            return {"action": "call"}
        return {"action": "check"} if state["can_check"] else {"action": "fold"}
    strength = made_hand(state)
    strong = strength not in ("High Card", "Pair")
    if strong and legal["can_raise"]:
        return {"action": "raise", "amount": min(legal["max_raise_to"],
                                                 max(legal["min_raise_to"], state["current_bet"] + pot // 2))}
    if state["can_check"]:
        return {"action": "check"}
    if strength == "Pair" and owed <= pot // 2:
        return {"action": "call"}
    return {"action": "call"} if strong else {"action": "fold"}
