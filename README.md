# Early Talent Identification in Football

End-to-end data project focused on identifying high-potential young football players by combining FIFA game data (static attributes) with Transfermarkt market-value data (dynamic, real-world signals).

## Project Objective

Build an analytical workflow to detect early indicators of future player value growth using:

- large-scale FIFA player data analysis with PySpark SQL
- exploratory statistical analysis by age, nationality, and position
- young-player potential screening (age < 21)
- Transfermarkt scraping for market value, contract information, and value timeline

## Repository Structure

- `notebooks/01_fifa_spark_eda.ipynb`: exploratory analysis of FIFA dataset with PySpark SQL
- `notebooks/02_transfermarkt_scrape.ipynb`: Transfermarkt scraping notebook and market value evolution plots
- `src/fifa_spark_eda.py`: script version of core Spark SQL analysis
- `src/transfermarkt_scraper.py`: script version of Transfermarkt scraping workflow
- `reports/ProyectoFinalBigData-Isunza_Valdes.pdf`: project report
- `data/processed/`: optional output directory for cleaned exports

## Main Analyses

1. Distribution of players by age and nationality
2. Average pace/shooting/passing/dribbling by age and nationality
3. Top 10 players under 21 with highest potential
4. Average attribute profile by club position
5. Average market value by nationality
6. Market value trajectory analysis for selected high-potential players

## Key Tools

- Python
- PySpark SQL
- Pandas
- Matplotlib / Seaborn
- BeautifulSoup + Requests
- BigQuery (optional export target)

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. If running Spark analysis, ensure your dataset path is available (local or HDFS).

## Running the Scripts

Spark EDA:

```bash
python src/fifa_spark_eda.py
```

Transfermarkt scraper:

```bash
python src/transfermarkt_scraper.py
```

## Notes

- Transfermarkt data can change over time, so values and timelines may differ from prior runs.
- The notebook in `notebooks/02_transfermarkt_scrape.ipynb` includes BigQuery upload examples.
- For interview discussion, this project is useful to explain early-signal detection, uncertainty, and data-driven scouting decisions.
