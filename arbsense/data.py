import json

import pandas as pd

from . import stats


def __flatten_odds_data(odds_data: dict) -> dict:
    all_odds = {}
    for event in odds_data:
        odds = []
        for bookmaker in event.get("bookmakers"):
            for market in bookmaker.get("markets"):
                odds.append(
                    {
                        "bookmaker_key": bookmaker.get("key"),
                        "bookmaker_title": bookmaker.get("title"),
                        "sport_key": event.get("sport_key"),
                        "sport_title": event.get("sport_title"),
                        "commence_time": event.get("commence_time"),
                        "market": market.get("key"),
                        "last_update": market.get("last_update"),
                        "home_team": event.get("home_team"),
                        "away_team": event.get("away_team"),
                        "home_team_odds": market.get("outcomes")[0].get("price"),
                        "away_team_odds": market.get("outcomes")[1].get("price"),
                    }
                )

        all_odds[event.get("id")] = odds

    return all_odds


def surebet_already_tracked(
    surebets: list,
    event_id: str,
    bookmaker_a: str,
    bookmaker_b: str,
    market: str,
) -> bool:
    for surebet in surebets:
        if (
            (surebet.get("event_id") == event_id)
            and surebet.get("market") == market
            and (
                (surebet.get("bookmaker_a") == bookmaker_a)
                or (surebet.get("bookmaker_a") == bookmaker_b)
            )
        ):
            return True

    return False


def get_surebets(investment_usd: int, odds_data: dict) -> pd.DataFrame:
    all_odds = __flatten_odds_data(odds_data=odds_data)

    surebets = []
    for event_id, odds in all_odds.items():
        for odds_a in odds:
            for odds_b in reversed(odds):
                if (odds_a.get("bookmaker_key") == odds_b.get("bookmaker_key")) or (
                    odds_a.get("market") != odds_b.get("market")
                ):
                    continue

                if surebet_already_tracked(
                    surebets=surebets,
                    event_id=event_id,
                    bookmaker_a=odds_a.get("bookmaker_key"),
                    bookmaker_b=odds_b.get("bookmaker_key"),
                    market=odds_a.get("market"),
                ):
                    continue

                is_profit, profit_percent, bet_a, bet_b = stats.compute_arbitrage(
                    investment_usd=investment_usd,
                    odds_a=odds_a.get("home_team_odds"),
                    odds_b=odds_b.get("away_team_odds"),
                )

                if is_profit:
                    surebets.append(
                        {
                            "event_id": event_id,
                            "sport_key": odds_a.get("sport_key"),
                            "sport_title": odds_a.get("sport_title"),
                            "commence_time": odds_a.get("commence_time"),
                            "market": odds_a.get("market"),
                            "last_update": odds_a.get("last_update"),
                            "home_team": odds_a.get("home_team"),
                            "away_team": odds_a.get("away_team"),
                            "bookmaker_a": odds_a.get("bookmaker_key"),
                            "bookmaker_b": odds_b.get("bookmaker_key"),
                            "bookmaker_a_home_team_odds": odds_a.get("home_team_odds"),
                            "bookmaker_b_home_team_odds": odds_b.get("home_team_odds"),
                            "bookmaker_a_away_team_odds": odds_a.get("away_team_odds"),
                            "bookmaker_b_away_team_odds": odds_b.get("away_team_odds"),
                            "profit_percent": round(profit_percent, 2),
                            "bet_a_usd": round(bet_a, 2),
                            "bet_b_usd": round(bet_b, 2),
                            "profit_usd": round(
                                investment_usd * (profit_percent / 100), 2
                            ),
                        }
                    )

    return pd.DataFrame(surebets)


def save_odds_data(odds_data: dict, name: str) -> None:
    with open(f"./data/{name}", "w") as f:
        f.write(json.dumps(odds_data))


def load_odds_data(name: str) -> dict:
    with open(f"./data/{name}") as f:
        odds_data = json.load(f)

    return odds_data
