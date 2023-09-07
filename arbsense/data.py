import json

import pandas as pd

from . import stats

# According to https://docs.google.com/spreadsheets/d/1WXH4lamqd0ixdsTvAu4FqrOSMRrqiX8Cs2n96Rg6RPM/edit#gid=297718827
# and: https://the-odds-api.com/sports-odds-data/bookmaker-apis.html#us-bookmakers
VALID_CO_BOOKMAKERS_ON_ODDS_API = {
    "barstool": "https://barstoolsportsbook.com/",
    "betmgm": "https://sports.co.betmgm.com/en/sports",
    "betrivers": "https://co.betrivers.com/?page=landing",
    "betway": "https://co.betway.com/",
    "williamhill_us": "https://caesars.com/sportsbook-and-casino/co/",
    "draftkings": "https://sportsbook.draftkings.com/",
    "fanduel": "https://co.sportsbook.fanduel.com/",
    "pointsbet": "https://co.pointsbet.com/",
    "sisportsbook": "https://www.sisportsbook.com/",
    "superbook": "https://co.superbook.com/sports",
    "tipico_us": "https://sportsbook-co.tipico.us/home",
}


def parse_surebets(investment_usd: int, odds_data: dict) -> pd.DataFrame:
    def flatten_odds_data_to_binary_outcomes(odds_data: dict) -> dict:
        all_odds = {}
        for event in odds_data:
            odds = []
            for bookmaker in event.get("bookmakers"):
                for market in bookmaker.get("markets"):
                    if len(market.get("outcomes")) != 2:
                        continue

                    odds.append(
                        {
                            "book_key": bookmaker.get("key"),
                            "book_title": bookmaker.get("title"),
                            "sport_key": event.get("sport_key"),
                            "sport_title": event.get("sport_title"),
                            "commence_time": event.get("commence_time"),
                            "market": market.get("key"),
                            "last_update": market.get("last_update"),
                            "team_a": event.get("home_team"),
                            "team_b": event.get("away_team"),
                            "odds_team_a": market.get("outcomes")[0].get("price"),
                            "odds_team_b": market.get("outcomes")[1].get("price"),
                        }
                    )

            all_odds[event.get("id")] = odds

        return all_odds

    def surebet_already_tracked(
        surebets: list,
        event_id: str,
        book_a: str,
        book_b: str,
        market: str,
    ) -> bool:
        for surebet in surebets:
            if (
                (surebet.get("event_id") == event_id)
                and surebet.get("market") == market
                and (
                    (surebet.get("book_a") == book_a)
                    or (surebet.get("book_a") == book_b)
                )
            ):
                return True

        return False

    all_odds = flatten_odds_data_to_binary_outcomes(odds_data=odds_data)

    surebets = []
    for event_id, book_odds in all_odds.items():
        for odds_book_a in book_odds:
            for odds_book_b in reversed(book_odds):
                if (odds_book_a.get("book_key") == odds_book_b.get("book_key")) or (
                    odds_book_a.get("market") != odds_book_b.get("market")
                ):
                    continue

                if surebet_already_tracked(
                    surebets=surebets,
                    event_id=event_id,
                    book_a=odds_book_a.get("book_key"),
                    book_b=odds_book_b.get("book_key"),
                    market=odds_book_a.get("market"),
                ):
                    continue

                arbitrages = stats.compute_arbitrages(
                    investment_usd=investment_usd,
                    odds_book_a=odds_book_a,
                    odds_book_b=odds_book_b,
                )

                for arbitrage in arbitrages:
                    surebets.append(
                        {
                            "event_id": event_id,
                            "sport_key": odds_book_a.get("sport_key"),
                            "sport_title": odds_book_a.get("sport_title"),
                            "commence_time": odds_book_a.get("commence_time"),
                            "market": odds_book_a.get("market"),
                            "last_update": odds_book_a.get("last_update"),
                            "team_a": odds_book_a.get("team_a"),
                            "team_b": odds_book_a.get("team_b"),
                            "book_a": odds_book_a.get("book_key"),
                            "book_a_url": VALID_CO_BOOKMAKERS_ON_ODDS_API.get(
                                odds_book_a.get("book_key")
                            ),
                            "odds_book_a_team_a": odds_book_a.get("odds_team_a"),
                            "odds_book_a_team_b": odds_book_a.get("odds_team_b"),
                            "book_b": odds_book_b.get("book_key"),
                            "book_b_url": VALID_CO_BOOKMAKERS_ON_ODDS_API.get(
                                odds_book_b.get("book_key")
                            ),
                            "odds_book_b_team_a": odds_book_b.get("odds_team_a"),
                            "odds_book_b_team_b": odds_book_b.get("odds_team_b"),
                            "team_a_bet_size_usd": round(
                                arbitrage.get("team_a_bet_size_usd"), 2
                            ),
                            "place_team_a_bet_with": arbitrage.get(
                                "place_team_a_bet_with"
                            ),
                            "team_b_bet_size_usd": round(
                                arbitrage.get("team_b_bet_size_usd"), 2
                            ),
                            "place_team_b_bet_with": arbitrage.get(
                                "place_team_b_bet_with"
                            ),
                            "total_bet_size_usd": round(
                                arbitrage.get("total_bet_size_usd"), 2
                            ),
                            "profit_percent": round(arbitrage.get("profit_percent"), 2),
                            "profit_usd": round(arbitrage.get("profit_usd"), 2),
                        }
                    )

    return pd.DataFrame(surebets)


def save_odds_data(odds_data: dict, absolute_path: str) -> None:
    with open(absolute_path, "w") as f:
        f.write(json.dumps(odds_data))


def load_odds_data(absolute_path: str) -> dict:
    with open(absolute_path) as f:
        odds_data = json.load(f)

    return odds_data
