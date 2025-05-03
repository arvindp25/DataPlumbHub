from pyspark.sql import SparkSession
import pyspark.sql.functions as f
import pyspark.sql.types as t
import os
import argparse
from pyspark.sql.types import StructType, StructField, StringType, BooleanType, LongType, TimestampType, MapType

# Define the schema based on the Wikimedia JSON message
schema = StructType([
    StructField("$schema", StringType()),
    StructField("meta", StructType([
        StructField("uri", StringType()),
        StructField("request_id", StringType()),
        StructField("id", StringType()),
        StructField("dt", StringType()),  # ISO timestamp string
        StructField("domain", StringType()),
        StructField("stream", StringType()),
        StructField("topic", StringType()),
        StructField("partition", LongType()),
        StructField("offset", LongType())
    ])),
    StructField("id", LongType()),
    StructField("type", StringType()),
    StructField("namespace", LongType()),
    StructField("title", StringType()),
    StructField("title_url", StringType()),
    StructField("comment", StringType()),
    StructField("timestamp", LongType()),
    StructField("user", StringType()),
    StructField("bot", BooleanType()),
    StructField("notify_url", StringType()),
    StructField("minor", BooleanType()),
    StructField("patrolled", BooleanType()),
    StructField("length", StructType([
        StructField("old", LongType()),
        StructField("new", LongType())
    ])),
    StructField("revision", StructType([
        StructField("old", LongType()),
        StructField("new", LongType())
    ])),
    StructField("server_url", StringType()),
    StructField("server_name", StringType()),
    StructField("server_script_path", StringType()),
    StructField("wiki", StringType()),
    StructField("parsedcomment", StringType())
])

parser = argparse.ArgumentParser()

parser.add_argument("--streaming_bucket", required=True)
parser.add_argument("--staging_bucket", required=True)

args = parser.parse_args()

spark = SparkSession.builder.master("yarn").appName("WikiMedia Streaming").config("temporaryGcsBucket", args.staging_bucket).getOrCreate()

# Read JSON files as they appear (line-delimited JSON per file)
sdf = spark.readStream \
    .format("json") \
    .schema(schema) \
    .option("maxFilesPerTrigger", 1) \
    .load(args.streaming_bucket)

sdf = sdf.withColumn("datetime" ,f.from_unixtime(f.col('timestamp')))
sdf= sdf.withColumn("minute", f.date_format(f.col('datetime'), "mm"))
df_edit_per_minute = sdf.withWatermark("10 secondss").groupBy(["minute"]).agg(f.count(f.col("id")).alias("edit_per_minute"))


query = df_edit_per_minute.writeStream.format("console").outputMode("update").trigger(processingTime = "2 second").start()

query.awaitTermination(120)

query.stop()