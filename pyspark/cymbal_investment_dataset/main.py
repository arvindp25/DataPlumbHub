from pyspark.sql import SparkSession
import os
from py4j.protocol import Py4JJavaError
import sys

staging_bucket = sys.argv[3]

def clean_column_name(name):
    return name.replace("(", "_").replace(")", "").replace(" ", "_")



def init_sparksession(appname = "CymbalInvestmentPortfolio" ):
    return SparkSession.builder.master('yarn').appName("CymbalInvestmentPortfolio").config("temporaryGcsBucket", staging_bucket).getOrCreate()

def load_source_table (spark, source_table):
    try:
        table_df = spark.read.format('bigquery').option('table', source_table).option('inferSchema', "true").load()
    except Py4JJavaError as e:
        print(f"Table {source_table} not found.")
        raise
    print("Current df size:", (table_df.count(), len(table_df.columns)))
    print("Columns:", table_df.columns)

    return table_df

def agg_dataframe(df):
    agg_df = df.groupBy(["symbol", "tradedate"]).agg({"StrikePrice": "avg", "Quantity": "count"})
    return agg_df

def dump_df_to_bq(df,dest_table):
    df.write.format('bigquery').option('table', dest_table).mode("overwrite").save()

def main():
    source_table = sys.argv[1]
    dest_table = f"{sys.argv[2]}.cymbal-investment-portfolio"


    # init
    spark = init_sparksession()
    df = load_source_table(spark,source_table=source_table)
    df = agg_dataframe(df)
    # Rename all columns dynamically
    new_column_names = {col: clean_column_name(col) for col in df.columns}
    for old_name, new_name in new_column_names.items():
        df = df.withColumnRenamed(old_name, new_name)

    dump_df_to_bq(df, dest_table)


        



