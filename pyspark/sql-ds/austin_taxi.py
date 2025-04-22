from pyspark.sql import SparkSession
from pyspark.sql.window import Window
import pyspark.sql.functions as f
import sys 
from py4j.protocol import Py4JJavaError

staging_bucket = sys.argv[3]


def init_sparksession(appname = "austin_taxi"):
    return SparkSession.builder.master("yarn").appName(appname).config("temporaryGcsBucket", staging_bucket) \
    .getOrCreate()


    