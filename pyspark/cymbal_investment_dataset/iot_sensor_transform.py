from pyspark.sql import SparkSession
from pyspark.sql.window import Window
from pyspark.sql.functions import udf, col
from py4j.protocol import Py4JJavaError
import sys
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="my-agent")

def init_sparksession(appname = "sensor_data"):
    return SparkSession.builder.master("yarn").appName(appname)

def load_source_table(spark,source_table):
    try:
        table_df =spark.read.format("bigquery").option('table', source_table).option("temporaryGcsBucket", staging_bucket).getOrCreate()
    except Py4JJavaError as e:
        print(f"Table {source_table} not found.")
        raise
    print("Current df size:", table_df.count(), table_df.columns)

    return table_df

@udf("string")
def get_address(latitude, longitude):
    try:
        location = geolocator.reverse(f"{latitude}, {longitude}")
    except:
        location = "Unknown"
    return location


def transform_df(df):
    df = df.withColumn('zip', get_address(col('location.latitude'), col('location.longitude')))
    return df

def dump_df_to_bq(df, dest_table):
    df.write.format("bigquery").option("table", dest_table).mode("overwrite").save()


def main():
    source_table = sys.argv[1]
    dest_table = f"{sys.argv[2]}.iot-sensor-address"
        # init
    spark = init_sparksession()
    df = load_source_table(spark,source_table=source_table)
    df = transform_df(df)
    dump_df_to_bq(df, dest_table)
    # Rename all columns dynamically

if __name__ == "__main__":
    main()

