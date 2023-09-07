def compute_arbitrages(
    investment_usd: float, odds_book_a: dict, odds_book_b: dict
) -> list[dict]:
    # Parse odds from both books
    odds_book_a_team_a = odds_book_a.get("odds_team_a")
    odds_book_a_team_b = odds_book_a.get("odds_team_b")
    odds_book_b_team_a = odds_book_b.get("odds_team_a")
    odds_book_b_team_b = odds_book_b.get("odds_team_b")

    # Compute implied probabilities
    ip_book_a_team_a = 1 / odds_book_a_team_a
    ip_book_a_team_b = 1 / odds_book_a_team_b

    ip_book_b_team_a = 1 / odds_book_b_team_a
    ip_book_b_team_b = 1 / odds_book_b_team_b

    total_ip_team_a = ip_book_a_team_a + ip_book_b_team_b
    total_ip_team_b = ip_book_b_team_a + ip_book_a_team_b

    # Detect arbitrage opportunities (when total implied probability < 1)
    arbitrages = []
    if total_ip_team_a < 1:
        team_a_bet_size_usd = (investment_usd * ip_book_a_team_a) / odds_book_a_team_a
        team_b_bet_size_usd = (investment_usd * ip_book_b_team_b) / odds_book_b_team_b

        arbitrages.append(
            {
                "total_bet_size_usd": team_a_bet_size_usd + team_b_bet_size_usd,
                "team_a_bet_size_usd": team_a_bet_size_usd,
                "team_b_bet_size_usd": team_b_bet_size_usd,
                "place_team_a_bet_with": odds_book_a.get("book_key"),
                "place_team_b_bet_with": odds_book_b.get("book_key"),
                "profit_percent": (1 - total_ip_team_a) * 100,
                "profit_usd": (1 - total_ip_team_a) * investment_usd,
            }
        )

    if total_ip_team_b < 1:
        team_a_bet_size_usd = (investment_usd * ip_book_b_team_a) / odds_book_b_team_a
        team_b_bet_size_usd = (investment_usd * ip_book_a_team_b) / odds_book_a_team_b

        arbitrages.append(
            {
                "total_bet_size_usd": team_a_bet_size_usd + team_b_bet_size_usd,
                "team_a_bet_size_usd": team_a_bet_size_usd,
                "team_b_bet_size_usd": team_b_bet_size_usd,
                "place_team_a_bet_with": odds_book_b.get("book_key"),
                "place_team_b_bet_with": odds_book_a.get("book_key"),
                "profit_percent": (1 - total_ip_team_b) * 100,
                "profit_usd": (1 - total_ip_team_b) * investment_usd,
            }
        )

    return arbitrages
