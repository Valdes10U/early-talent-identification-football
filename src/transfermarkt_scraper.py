"""Transfermarkt market-value scraper used in the project.

This script fetches:
- current market value
- contract expiry
- last market-value update
- market value development timeline
"""

from __future__ import annotations

from datetime import datetime
import re

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0"
    )
}


def extract_date(input_string: str) -> str | None:
    pattern = r"Last update:\\s+([A-Za-z]+\\s+\\d{1,2},\\s+\\d{4})"
    match = re.search(pattern, input_string)
    return match.group(1) if match else None


def plot_market_value_history(graph_response: requests.Response, player_name: str) -> None:
    data = graph_response.json()
    points = data.get("list", [])
    if not points:
        return

    timestamps = [point["x"] for point in points]
    market_values = [point["y"] for point in points]
    clubs = [point.get("verein", "") for point in points]
    ages = [point.get("age", "") for point in points]

    dates = [datetime.fromtimestamp(ts / 1000) for ts in timestamps]

    plt.figure(figsize=(12, 6))
    plt.plot(dates, market_values, marker="o", linestyle="-", color="b")

    for i, _ in enumerate(points):
        plt.annotate(
            f"{clubs[i]} - {ages[i]}",
            (dates[i], market_values[i]),
            textcoords="offset points",
            xytext=(0, 10),
            ha="center",
        )

    plt.xlabel("Date")
    plt.ylabel("Market Value (EUR)")
    plt.title(f"Market Value Development for {player_name}")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def get_player_info(url: str) -> dict:
    player_id = url.rstrip("/").split("/")[-1]
    response = requests.get(url, headers=HEADERS, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, "html.parser")

    name_node = soup.select_one('h1[class="data-header__headline-wrapper"]')
    player_name = name_node.text.split("\n")[-1].strip() if name_node else "Unknown"

    contract_match = re.search(r"Contract expires: (.*)", soup.text)
    player_contract_expiry = contract_match.group(1) if contract_match else np.nan

    market_value_match = re.search(r"€(.*)", soup.text)
    market_value = market_value_match.group(0).split(" ")[0] if market_value_match else np.nan
    market_value_date_text = market_value_match.group(0) if market_value_match else ""

    graph_response = requests.get(
        f"https://www.transfermarkt.us/ceapi/marketValueDevelopment/graph/{player_id}",
        headers=HEADERS,
        timeout=30,
    )
    graph_response.raise_for_status()

    return {
        "name": player_name,
        "market_value": market_value,
        "contract_expiry": player_contract_expiry,
        "last_update_tm": extract_date(market_value_date_text),
        "date_logged": datetime.now().strftime("%Y-%m-%d"),
        "graph_response": graph_response,
    }


def collect_players(player_urls: list[str], plot_first_n: int = 10) -> pd.DataFrame:
    records = []

    for index, url in enumerate(player_urls):
        try:
            player = get_player_info(url)
            print(f"Player name: {player['name']}")
            print(f"Current market value: {player['market_value']}")
            print(f"Contract expiry date: {player['contract_expiry']}\n")

            if index < plot_first_n:
                plot_market_value_history(player["graph_response"], player["name"])

            records.append(
                {
                    "Name": player["name"],
                    "Market Value": player["market_value"],
                    "Contract Expiry Date": player["contract_expiry"],
                    "Last Update TM": player["last_update_tm"],
                    "Date Logged": player["date_logged"],
                }
            )
        except Exception as exc:
            print(f"Error fetching {url}: {exc}")

    return pd.DataFrame(records)


def upload_to_bigquery(df: pd.DataFrame, table: str, project_id: str) -> None:
    import pandas_gbq

    pandas_gbq.to_gbq(df, table, project_id=project_id, if_exists="append")


if __name__ == "__main__":
    urls = [
        "https://www.transfermarkt.com/kylian-mbappe/profil/spieler/342229",
        "https://www.transfermarkt.com/gianluigi-donnarumma/profil/spieler/315858",
        "https://www.transfermarkt.com/erling-haaland/profil/spieler/418560",
    ]
    result_df = collect_players(urls, plot_first_n=3)
    print(result_df.head())
