import pandas as pd

from . import stats


def get_surebets(odds_data: dict) -> pd.DataFrame:
    surebets = []

    for event in odds_data:
        team_a, team_b = event.get("home_team"), event.get("away_team")

        bookmaker_odds = []
        for bookmaker in event.get("bookmakers"):
            book = bookmaker.get("key")
            markets = bookmaker.get("markets")

            for market in markets:
                pass

            pass

        odds_list = []

        for site in event["sites"]:
            odds = site["odds"]["h2h"]
            odds_list.append((site["site_nice"], odds))

        for i in range(len(odds_list)):
            for j in range(i + 1, len(odds_list)):
                site_a, odds_a = odds_list[i]
                site_b, odds_b = odds_list[j]

                profit, bet_a, bet_b = stats.compute_surebet(odds_a[0], odds_b[0])

                if profit:
                    surebets.append(
                        {
                            "Team A": team_a,
                            "Team B": team_b,
                            "Site A": site_a,
                            "Site B": site_b,
                            "Odds A": odds_a[0],
                            "Odds B": odds_b[0],
                            "Profit %": round(profit, 2),
                            "Bet A": round(bet_a, 2),
                            "Bet B": round(bet_b, 2),
                            "Timestamp": event["commence_time"],
                        }
                    )
