from pyspark.sql import SparkSession
import os
from py4j.protocol import Py4JJavaError

spark = SparkSession.builder.master('yarn').appName("CymbalInvestmentPortfolio")

bucket = os.getenv("STAGING_BUCKET")
spark.conf.set("temporaryGcsBucket", bucket)

source_table = os.getenv("BQ_SOURCE_TABLE")
dest_table = os.getenv("BQ_DEST_TABLE")

try:
    table_df = spark.read.format('bigquery').option('table', source_table).option('inferSchema', "true")
except Py4JJavaError as e:
    print(f"Table {source_table} not found.")
    raise

agg_df = table_df.groupBy(["symbol", "tradedate"]).agg({"StrikePrice": "avg", "Quantity": "count"})

agg_df.write.format('bigquery').option('table', dest_table)