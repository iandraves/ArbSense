from numba import njit


@njit
def compute_arbitrage(investment_usd: float, odds_a: float, odds_b: float) -> tuple:
    implied_prob_a = 1 / odds_a
    implied_prob_b = 1 / odds_b
    total_implied_prob = implied_prob_a + implied_prob_b

    if total_implied_prob < 1:
        profit_percentage = (1 - total_implied_prob) * 100

        bet_a = (investment_usd * implied_prob_a) / odds_a
        bet_b = (investment_usd * implied_prob_b) / odds_b

        return True, profit_percentage, bet_a, bet_b
    else:
        return False, None, None, None
