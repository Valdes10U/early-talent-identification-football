# Early Talent Identification in Football

Data science project that combines static player attributes (FIFA dataset) with dynamic market signals (Transfermarkt scraping) to identify high-potential young players and analyze early career value patterns.

## Why This Project

Scouting and talent investment decisions are made under uncertainty. This project explores how historical player attributes and market-value evolution can support earlier and more structured decision-making.

The analysis is academically grounded and portfolio-oriented, with a focus on transparency and reproducibility.

## Scope

- FIFA player analytics at scale with PySpark SQL
- exploratory analysis by age, nationality, and position
- ranking young players by potential (age < 21)
- Transfermarkt scraping for market value, contract expiry, and timeline history
- optional export of scraped records to BigQuery

## Repository Structure

- `notebooks/01_fifa_spark_eda.ipynb`: Spark SQL exploratory analysis notebook
- `notebooks/02_transfermarkt_scrape.ipynb`: Transfermarkt scraping notebook
- `src/fifa_spark_eda.py`: script version of the Spark SQL workflow
- `src/transfermarkt_scraper.py`: script version of the Transfermarkt workflow
- `reports/ProyectoFinalBigData-Isunza_Valdes.pdf`: full project report
- `data/processed/`: local output directory for optional exports

## Analysis Covered

1. Age distribution by nationality
2. Mean pace, shooting, passing, and dribbling by age and nationality
3. Top young players by potential
4. Mean attribute profile by club position
5. Average market value by nationality
6. Market-value trajectory visualizations for selected players

## Tech Stack

- Python
- PySpark SQL
- Pandas
- Matplotlib and Seaborn
- Requests and BeautifulSoup
- BigQuery (optional)

## Setup

1. Create a Python virtual environment.
2. Activate the environment.
3. Install dependencies.

```bash
pip install -r requirements.txt
```

4. Ensure Spark is available in your environment.
5. Update dataset path in the notebook or script if your `male_players.csv` location differs.

## How To Run

Run Spark EDA script:

```bash
python src/fifa_spark_eda.py
```

Run Transfermarkt scraper script:

```bash
python src/transfermarkt_scraper.py
```

## Practical Notes

- Transfermarkt values evolve over time, so reruns may produce different numbers.
- Scraping behavior may change as site structure changes.
- In the original project environment, parts of the workflow used HDFS/Dataproc constraints documented in the report.

## Interview Talking Points

- framing player scouting as early-signal detection under uncertainty
- combining static and dynamic data sources into one analytical workflow
- using PySpark SQL for scalable exploration before deeper modeling
- moving from descriptive insights to investment-style decision hypotheses

## Next Extensions

- add a unified feature table that joins FIFA and Transfermarkt records by player
- track model-ready features such as value-growth slope and volatility
- formalize evaluation with time-based train/test splits for forward-looking prediction
