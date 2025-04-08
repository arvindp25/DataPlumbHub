from pyspark.sql import SparkSession
from pyspark.sql.window import Window
from pyspark.sql.functions import udf, col
from uszipcode import SearchEngine
from py4j.protocol import Py4JavaError
import sys
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="my-agent")

def init_sparksession(appname = "sensor_data"):
    return SparkSession.builder.master("yarn").appName(appname)

def load_source_table(spark,source_table):
    try:
        table_df =spark.read.format("bigquery").option('table', source_table).option("temporaryGcsBucket", staging_bucket).getOrCreate()
    except Py4JavaError as e:
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
    df.withColumn('zip', get_address(col('location.latitude'), col('location.longitude')))

