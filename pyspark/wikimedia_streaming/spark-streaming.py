from pyspark.sql import SparkSession
import pyspark.sql.functions as f
import pyspark.sql.types as t
import os
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--streaming_bucket", required=True)
parser.add_argument("--staging_bucket", required=True)

args = parser.parse_args()

spark = SparkSession.builder.master("yarn").appName("WikiMedia Streaming").config("temporaryGcsBucket", args.staging_bucket).getOrCreate()

# Read JSON files as they appear (line-delimited JSON per file)
sdf = spark.readStream \
    .format("json") \
    .option("maxFilesPerTrigger", 1) \
    .load(args.streaming_bucket)



query = sdf.writeStream.format("console").outputMode("append").trigger(processingTime = "2 second").start()

query.awaitTermination(120)

query.stop()