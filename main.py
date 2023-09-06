import os

import betiq
from dotenv import load_dotenv

import arbsense

load_dotenv()


def main():
    # odds_data = betiq.get_odds(
    #     api_key=os.getenv("THE_ODDS_API_API_KEY"),
    #     bookmakers=list(arbsense.data.VALID_CO_BOOKMAKERS_ON_ODDS_API.keys()),
    # )

    # arbsense.data.save_odds_data(
    #     odds_data=odds_data, absolute_path="./sample_data/all_upcoming_co_4.json"
    # )

    odds_data = arbsense.data.load_odds_data(
        absolute_path="./sample_data/all_upcoming_co_4.json"
    )

    surebets_df = arbsense.data.get_surebets(investment_usd=1000, odds_data=odds_data)

    if surebets_df.empty:
        print("No surebets detected.")
    else:
        surebets_df = surebets_df.sort_values(by="profit_usd", ascending=False)
        print(surebets_df)
        surebets_df.to_csv("surebets.csv")


if __name__ == "__main__":
    main()
