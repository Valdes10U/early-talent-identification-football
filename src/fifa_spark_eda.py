"""FIFA players exploratory analysis using PySpark SQL.

This script reproduces the SQL-driven analysis flow used in the project:
- top percentile player filtering
- attribute summary statistics
- age distribution by nationality
- attribute averages by age and nationality
- top young players by potential
- attribute averages by club position
- average market value by nationality
"""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
from pyspark.sql import SparkSession


@dataclass
class AnalysisConfig:
    csv_path: str = "hdfs:///user/usuario/datasets/csv/male_players.csv"
    top_percentile: int = 95


RELEVANT_ATTRIBUTES = [
    "movement_agility",
    "skill_ball_control",
    "power_strength",
    "attacking_crossing",
    "attacking_finishing",
    "attacking_heading_accuracy",
    "defending_marking_awareness",
    "defending_standing_tackle",
    "defending_sliding_tackle",
    "mentality_aggression",
    "mentality_interceptions",
    "mentality_positioning",
]


def create_spark_session(app_name: str = "Analisis de FIFA Players con SQL") -> SparkSession:
    return SparkSession.builder.appName(app_name).getOrCreate()


def load_fifa_players(spark: SparkSession, csv_path: str):
    df = (
        spark.read.format("csv")
        .option("header", "true")
        .option("inferSchema", "true")
        .load(csv_path)
    )
    df.createOrReplaceTempView("fifa_players")
    return df


def query_top_players(spark: SparkSession, percentile: int):
    query = f"""
        SELECT *
        FROM fifa_players
        WHERE overall >= (
            SELECT approx_percentile(overall, {percentile}/100.0)
            FROM fifa_players
        )
    """
    return spark.sql(query)


def query_summary_stats(spark: SparkSession, top_players_view: str = "top_players") -> pd.DataFrame:
    summary_stats = pd.DataFrame()
    for attribute in RELEVANT_ATTRIBUTES:
        query = f"""
            SELECT
                '{attribute}' AS attribute,
                AVG({attribute}) AS avg_value,
                MIN({attribute}) AS min_value,
                MAX({attribute}) AS max_value,
                STDDEV({attribute}) AS stddev_value
            FROM fifa_players
            WHERE player_id IN (SELECT player_id FROM {top_players_view})
        """
        stats_df = spark.sql(query).toPandas()
        summary_stats = pd.concat([summary_stats, stats_df], ignore_index=True)
    return summary_stats


def query_age_distribution(spark: SparkSession) -> pd.DataFrame:
    query = """
        SELECT nationality_name, age, COUNT(*) AS num_players
        FROM fifa_players
        GROUP BY nationality_name, age
        ORDER BY nationality_name, age
    """
    return spark.sql(query).toPandas()


def query_avg_attributes_by_age_nationality(spark: SparkSession) -> pd.DataFrame:
    query = """
        SELECT nationality_name, age,
               AVG(pace) AS avg_pace,
               AVG(shooting) AS avg_shooting,
               AVG(passing) AS avg_passing,
               AVG(dribbling) AS avg_dribbling
        FROM fifa_players
        GROUP BY nationality_name, age
        ORDER BY nationality_name, age
    """
    return spark.sql(query).toPandas()


def query_top_young_players(spark: SparkSession, age_limit: int = 21, top_n: int = 10) -> pd.DataFrame:
    query = f"""
        SELECT short_name, nationality_name, age, potential
        FROM fifa_players
        WHERE age < {age_limit}
        GROUP BY short_name, age, nationality_name, potential
        ORDER BY potential DESC
        LIMIT {top_n}
    """
    return spark.sql(query).toPandas()


def query_avg_attributes_by_position(spark: SparkSession) -> pd.DataFrame:
    query = """
        SELECT club_position,
               AVG(pace) AS avg_pace,
               AVG(shooting) AS avg_shooting,
               AVG(passing) AS avg_passing,
               AVG(dribbling) AS avg_dribbling
        FROM fifa_players
        GROUP BY club_position
    """
    return spark.sql(query).toPandas()


def query_avg_market_value_by_nationality(spark: SparkSession) -> pd.DataFrame:
    query = """
        SELECT nationality_name,
               AVG(value_eur) AS avg_value_eur
        FROM fifa_players
        GROUP BY nationality_name
        ORDER BY avg_value_eur DESC
    """
    return spark.sql(query).toPandas()


def run_analysis(config: AnalysisConfig) -> None:
    spark = create_spark_session()
    try:
        _ = load_fifa_players(spark, config.csv_path)

        top_players_df = query_top_players(spark, config.top_percentile)
        top_players_df.createOrReplaceTempView("top_players")

        summary_stats = query_summary_stats(spark)
        age_distribution = query_age_distribution(spark)
        avg_attributes = query_avg_attributes_by_age_nationality(spark)
        young_players = query_top_young_players(spark)
        position_attributes = query_avg_attributes_by_position(spark)
        nationality_values = query_avg_market_value_by_nationality(spark)

        print("Summary stats sample:")
        print(summary_stats.head())
        print("\nAge distribution sample:")
        print(age_distribution.head())
        print("\nAverage attributes sample:")
        print(avg_attributes.head())
        print("\nTop young players sample:")
        print(young_players.head())
        print("\nPosition attributes sample:")
        print(position_attributes.head())
        print("\nNationality average market value sample:")
        print(nationality_values.head())
    finally:
        spark.stop()


if __name__ == "__main__":
    run_analysis(AnalysisConfig())
