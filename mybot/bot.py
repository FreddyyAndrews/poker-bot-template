"""
mybot: a simple, readable starting point. Improve it.

Strategy (deliberately basic):
- Preflop: score the two cards (pairs, high cards, suited, connected).
  Raise strong hands, call medium hands when the price is small, check
  when it's free, otherwise fold. Shove strong hands when short-stacked.
- Postflop: estimate equity against random hands for every opponent still
  in, compare it with the pot odds, and bet/raise when well ahead, call
  when the price is right, check when free, fold otherwise.

Known weaknesses to work on: it assumes opponents hold random hands
(real ranges are stronger after they bet), it never bluffs, it sizes
every bet the same, and it ignores position and the match history in
state["match_action_log"].

Every decision is explained with ctx.log, so `arena match hand MATCH:HAND`
and `arena decisions --bot mybot` show why it did what it did.
"""

from poker_harness.equity import equity

RANKS = "23456789TJQKA"
EQUITY_SAMPLES = 400        # Monte Carlo samples per postflop decision


def preflop_score(cards) -> float:
    """0 (worst) to about 1 (aces): a rough hand-strength score."""
    (r1, s1), (r2, s2) = cards
    hi, lo = sorted((RANKS.index(r1), RANKS.index(r2)), reverse=True)
    if hi == lo:
        return 0.5 + 0.5 * hi / 12                  # 22 = 0.5 ... AA = 1.0
    score = (hi + lo) / 24 * 0.6                    # high cards
    if s1 == s2:
        score += 0.06                               # suited
    if hi - lo == 1:
        score += 0.04                               # connected
    if hi == 12:
        score += 0.08                               # an ace
    return score


def raise_to(state, total: int) -> dict:
    """A raise to `total` chips this street, kept within the legal range."""
    legal = state["legal_actions"]
    total = max(legal["min_raise_to"], min(total, legal["max_raise_to"]))
    return {"action": "raise", "amount": total}


def decide(state, ctx):
    legal = state["legal_actions"]
    owed, pot, bb = state["amount_owed"], state["pot"], state["big_blind"]
    stack_bb = (state["your_stack"] + state["your_bet_this_street"]) / bb

    if state["street"] == "preflop":
        score = preflop_score(state["your_cards"])
        ctx.log("preflop", score=round(score, 2), owed=owed, stack_bb=round(stack_bb, 1))
        if score >= 0.75 and legal["can_raise"]:
            if stack_bb <= 15:
                return {"action": "all_in"}
            return raise_to(state, state["current_bet"] + 2 * max(bb, owed) + bb)
        if score >= 0.45 and owed <= 3 * bb:
            return {"action": "call"} if owed else {"action": "check"}
        return {"action": "check"} if state["can_check"] else {"action": "fold"}

    opponents = sum(1 for p in state["players"]
                    if p["state"] in ("active", "all_in") and p["seat"] != state["seat_to_act"])
    result = equity(["".join(state["your_cards"])] + ["any"] * max(1, opponents),
                    board="".join(state["community_cards"]),
                    iters=EQUITY_SAMPLES, seed=state["hand_num"])
    eq = result["players"][0]["equity"]
    price = owed / (pot + owed) if owed else 0.0
    ctx.log("postflop", equity=round(eq, 3), price=round(price, 3), opponents=opponents)

    if eq >= 0.7 and legal["can_raise"]:
        return raise_to(state, state["current_bet"] + int((pot + owed) * 0.66))
    if state["can_check"]:
        return {"action": "check"}
    if eq > price + 0.05:
        return {"action": "call"}
    return {"action": "fold"}
