import json
import os

import betiq
from dotenv import load_dotenv

import arbsense

load_dotenv()


def main():
    # odds_data = betiq.get_odds(
    #     api_key=os.getenv("THE_ODDS_API_KEY"), sport="baseball_mlb", regions=["us"]
    # )

    # with open("output.txt", "w") as f:
    #     f.write(json.dumps(odds_data))

    with open("output.json") as f:
        odds_data = json.load(f)

    print(odds_data)

    # surebets = arbsense.data.get_surebets(odds_data=odds_data)


if __name__ == "__main__":
    main()
