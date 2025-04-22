# Dataset: bigquery-public-data.new_york_citibike.citibike_trips

#     Find the top 3 stations with the lowest standard deviation in daily trip counts (i.e., consistent usage) in 2019.
#     Return:

#         start_station_name

#         std_dev_trips_per_day
#         Consider only stations with at least 200 days of usage and a minimum of 50 trips per day on average.

# with cte as (
# SELECT start_station_name,extract(date from starttime) day ,count(*) trip_count FROM `bigquery-public-data.new_york_citibike.citibike_trips`
# where extract(year from starttime) = 2017
# group by start_station_name, extract(date from starttime)
# ),
# more_than_200 as (
# select start_station_name, count(*) as days_used, avg(trip_count) avg_trips_per_day, STDDEV(trip_count) AS std_dev_trips_per_day  from cte
# group by start_station_name
# having count(*) >= 200 and avg_trips_per_day >=50
# )
# select * from more_than_200
# order by more_than_200.std_dev_trips_per_day limit 3


from pyspark.sql import SparkSession
from pyspark.sql.window import Window
import pyspark.sql.functions as f
from py4j.protocol import Py4JJavaError
import sys

staging_bucket = sys.argv[3]

def init_sparksession(appname = "citibike_trips"):
    return SparkSession.builder.master("yarn").appName(appname)\
    .config("temporaryGcsBucket", staging_bucket).getOrCreate()

def load_source_table(spark):
    try:
        table_df = spark.read.format('bigquery').option('table', sys.argv[1]).option('inferSchema', "true").load()
    except:
        print(f"Table {sys.argv[1]} not found.")
        raise
    print("Current df size:", (table_df.count(), len(table_df.columns)))
    print("Columns:", table_df.columns)
    return table_df


def transform_df(df):
    df = df.withColumn("start_date", f.to_date(f.col("starttime")))
    df = df.groupBy(["start_station_name", "start_date"]).agg(f.count("*").alias("trip_count"))
    df = df.groupBy(["start_station_name"]).agg(f.count("*").alias("days_used"),f.avg("trip_count").alias("avg_trip_count"),\
                                                f.stddev("trip_count").alias("std_dev_trips_per_day")
                                                )\
                                                .filter(f.col("avg_trip_count") >= 50 and f.col("days_used") >= 200)
    return df

def dump_df_to_bq(df, dest_table):
    df.write.format("bigquery").option("table", dest_table).mode("overwrite").save()

def main():
    source_table = sys.argv[1]
    dest_table = f"{sys.argv[2]}.citibike_trips_std_dev"

    spark = init_sparksession()
    df = load_source_table(spark)
    df= transform_df(df)

    dump_df_to_bq(df,dest_table)

if __name__ == "__main__":
    main()


