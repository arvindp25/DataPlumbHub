from pyspark.sql import SparkSession
import os
from py4j.protocol import Py4JJavaError
import sys

def clean_column_name(name):
    return name.replace("(", "_").replace(")", "").replace(" ", "_")

source_table = sys.argv[1]
dest_table = f"{sys.argv[2]}.cymbal-investment-portfolio"
bucket = sys.argv[3]
spark = SparkSession.builder.master('yarn').appName("CymbalInvestmentPortfolio").config("temporaryGcsBucket", bucket).getOrCreate()

try:
    table_df = spark.read.format('bigquery').option('table', source_table).option('inferSchema', "true").load()
except Py4JJavaError as e:
    print(f"Table {source_table} not found.")
    raise
print("Current df size:", (table_df.count(), len(table_df.columns)))
print("Columns:", table_df.columns)

agg_df = table_df.groupBy(["symbol", "tradedate"]).agg({"StrikePrice": "avg", "Quantity": "count"})



# Rename all columns dynamically
new_column_names = {col: clean_column_name(col) for col in agg_df.columns}
for old_name, new_name in new_column_names.items():
    agg_df = agg_df.withColumnRenamed(old_name, new_name)

agg_df.write.format('bigquery').option('table', dest_table).mode("overwrite").save()