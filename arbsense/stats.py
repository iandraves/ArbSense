def compute_surebet(investment: float, odds_a: float, odds_b: float) -> dict:
    implied_prob_a = 1 / odds_a
    implied_prob_b = 1 / odds_b
    total_implied_prob = implied_prob_a + implied_prob_b

    if total_implied_prob < 1:
        profit_percentage = (1 - total_implied_prob) * 100

        bet_a = (investment * implied_prob_a) / odds_a
        bet_b = (investment * implied_prob_b) / odds_b

        return {"profit_percentage": profit_percentage, "bet_a": bet_a, "bet_b": bet_b}
    else:
        return {"profit_percentage": None, "bet_a": None, "bet_b": None}
