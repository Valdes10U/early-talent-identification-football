# Interview Pitch Guide

## 30-Second Version

This project analyzes early talent identification in football by combining FIFA player attributes with Transfermarkt market-value history. I used PySpark SQL to explore large player datasets and identify young players with high potential, then added web-scraped market timelines to study how early signals relate to future value growth. The objective was to make scouting-style decisions more data-driven under uncertainty.

## 90-Second Version

I built this project in two parts. First, I used PySpark SQL on FIFA data to analyze distributions and patterns across age, nationality, position, and potential. This included ranking under-21 players, comparing average attributes like pace and dribbling, and profiling positions where these attributes are most relevant.

Second, I scraped Transfermarkt to enrich the analysis with real-world dynamic signals: current market value, contract expiry, and historical value development. That let me move from static snapshots to time-based value evolution, which is closer to an investment or risk lens.

The key learning was that combining static technical profiles with dynamic market behavior gives a stronger basis for early decision-making than either source alone.

## Role-Relevant Framing (Fintech/Credit Style)

Use these mappings when speaking to data science roles outside sports:

- Player potential: analogous to expected upside or future customer value
- Market value trajectory: analogous to risk-adjusted trend over time
- Under-21 filtering and ranking: analogous to candidate screening under constraints
- Combining FIFA + Transfermarkt: analogous to joining internal and external signals
- Uncertainty in early career prediction: analogous to early-stage credit or risk modeling

## Common Interview Questions and Answers

1. Why PySpark instead of only Pandas?
- The original analysis was designed for a big-data course context and SQL-style aggregation at scale. PySpark made grouped queries and percentile filtering practical and reproducible.

2. What was the hardest part technically?
- Data acquisition and environment setup: scraping dynamic pages, extracting player IDs, and handling infrastructure limitations around HDFS/cluster configuration.

3. What would you improve next?
- Build a joined player-level feature table and train a forward-looking model to predict future market-value growth with proper time splits.

4. How did you keep this analysis honest?
- I focused on transparent exploratory outputs and avoided claiming production deployment or guaranteed predictive performance.
