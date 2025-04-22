from pyspark.sql import SparkSession
from pyspark.sql.window import Window
import pyspark.sql.functions as f
import sys 
from py4j.protocol import Py4JJavaError

staging_bucket = sys.argv[3]


def init_sparksession(appname = "austin_taxi"):
    return SparkSession.builder.master("yarn").appName(appname).config("temporaryGcsBucket", staging_bucket) \
    .getOrCreate()

def load_source_table(spark, source_table_name):
    try:
        df = spark.read.format("bigquery").option("table", source_table_name) \
            .option("inferSchema", "true").load()
    except:
        print(f"Table {source_table_name} not found.")
        raise
    print("Current df size:", (df.count(), len(df.columns)))
    print("Columns:", df.columns)

def transform_df(df1, df2):
    """
      with cte as (
    select start_station_id, extract(hour from start_time) hour_of_day, count(trip_id) total_trips from bigquery-public-data.austin_bikeshare.bikeshare_trips bt
    group by start_station_id, hour_of_day
  ),
   rn as (
  select name as borough, hour_of_day, total_trips, rank() over (partition by name order by total_trips desc) rank_ from cte bt
  join bigquery-public-data.austin_bikeshare.bikeshare_stations bs
  on 
  bs.station_id = bt.start_station_id
  )
  select * except (rank_) from rn
  where rank_ =1
    """
    
    
    