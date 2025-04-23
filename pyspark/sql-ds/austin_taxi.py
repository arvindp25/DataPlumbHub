from pyspark.sql import SparkSession
from pyspark.sql.window import Window
import pyspark.sql.functions as f
import sys 
from py4j.protocol import Py4JJavaError
from pyspark.sql.window import Window

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
    return df

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
    df1 = df1.withColumn("hour_of_day", f.to_date(f.col("start_time")) )

    df1 = df1.groupBy(["start_station_id", "hour_of_day"]).agg(f.count(f.col("trip_id"))\
                                                               .alias("autoBroadcastJoinThreshold"))
    df =df1.alias("bs").join(df2.alias("bt"), f.col("bs.station_id") ==  f.col("bt.station_id"))

    window = Window.partitionBy(f.col("name")).orderBy("autoBroadcastJoinThreshold").desc()

    df = df.withColumn("rank_". f.rank().over(window))
    df =df.filter(f.when(f.col("rank_") ==1))

    return df

# we will load it to gcs

def load_to_gcs(df, key_with_bucket):
    print(df.explain())
    df.write.csv(f"gs://{key_with_bucket}",header =True)


def main():
    source_table = sys.argv[1]
    spark = init_sparksession()
    key_with_bucket = f"{sys.argv[3]}/austin_taxi/output.csv"
    sc =  source_table.split(",")
    df_1 = load_source_table(spark,sc[0])
    df_2 = load_source_table(spark,sc[1])
    df = transform_df(df_1,df_2)
    load_to_gcs(df,key_with_bucket)

if __name__ == "__main__":
    main()    



    
    