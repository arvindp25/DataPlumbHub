from pyspark.sql import SparkSession
import pyspark.sql.functions as f
import pyspark.sql.types as t
import os
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--subscription_id", required=True)
parser.add_argument("--staging_bucket", required=True)

args = parser.parse_args()

spark = SparkSession.master.builder.appName("WikiMedia Streaming").config("temporaryGcsBucket", args.staging_bucket).getOrcreate()

sdf = spark.readStream.format("pubsublite")\
    .option("pubsublite.subscription", args.subscription_id).load()


sdf = sdf.withColumn("data", sdf.data.cast(t.StringType()))

query = sdf.writeStream.format("console").outputMode("append").trigger(processingTime = "2 second").start()

query.awaitTermination(120)

query.stop()