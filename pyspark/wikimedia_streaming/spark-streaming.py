from pyspark.sql import SparkSession
import pyspark.sql.functions as f
import pyspark.sql.types as t
import os
import argparse
from pyspark.sql.types import StructType, StructField, StringType, BooleanType, LongType, TimestampType, MapType
import json

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
parser.add_argument("--table_name", required=True, type =json.loads)
args = parser.parse_args()


spark = SparkSession.builder.master("yarn").appName("WikiMedia Streaming").config("temporaryGcsBucket", args.staging_bucket).getOrCreate()

def write_to_bq(df,batch_id, table):
    df.write \
    .format("bigquery") \
    .option("table", table) \
    .option("writeMethod", "direct") \
    .option("mergeSchema", "true")\
    .mode("append").save()


# Read JSON files as they appear (line-delimited JSON per file)
sdf = spark.readStream \
    .format("json") \
    .schema(schema) \
    .option("maxFilesPerTrigger", 1) \
    .load(args.streaming_bucket)

sdf = sdf.withColumn("datetime", f.from_unixtime(f.col("timestamp")).cast("timestamp"))
sdf = sdf.withWatermark("datetime", "1 minute")
sdf= sdf.withColumn("minute", f.date_format(f.col('datetime'), "mm"))
# edit_per_minute
df_edit_per_minute = sdf.withWatermark("datetime", "1 minute").groupBy(f.window("datetime", "1 minute").alias("window")) \
.agg(f.count("*").alias("edit_count"))
df_edit_per_minute = df_edit_per_minute.withColumn("window", f.col("window").cast("string"))
# rolling avg
rolling_avg_df = sdf.withWatermark("datetime", "10 minutes") \
.groupBy(f.window("datetime", "5 minutes", "1 minute").alias("window")) \
.agg(f.count("*").alias("rolling_avg_edit_count"))
# user vs bot vs anon
sdf = sdf.withColumn("type_of_editor", f.when(f.col("bot") == "true", "Bot")\
                     .when(f.col('user').rlike(r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'), 'Anonymous')\
                        .otherwise('User'))

editing_count_df = sdf.groupBy(["type_of_editor"]).agg(f.count("*").alias("count_per_editor"))
print(args.table_name)

print(df_edit_per_minute.printSchema())

query_1 = df_edit_per_minute.writeStream.foreachBatch(lambda df, batch_id: write_to_bq(df,batch_id, args.table_name.get('editing_count')) ).outputMode("append").option("checkpointLocation",f"{args.staging_bucket}/checkpoints/edit_per_minute") \
    .start()

# query_2 = rolling_avg_df.writeStream.foreachBatch(lambda df, batch_id: write_to_bq(df,batch_id, args.table_name.get('rolling_avg'))).outputMode("append").option("checkpointLocation", f"{args.staging_bucket}/checkpoints/rolling_avg").start()

# query_2 =  rolling_avg_df.writeStream.format("console").outputMode("update").trigger(processingTime = "2 second").start()
# query_3 = editing_count_df.writeStream.foreachBatch(lambda df, batch_id:write_to_bq(df,batch_id, args.table_name.get('editing_count'))).outputMode("append").option("checkpointLocation", f"{args.staging_bucket}/checkpoints/editing_count").start()

query_1.awaitTermination(300)
# query_2.awaitTermination(300)
# query_3.awaitTermination(300)



query_1.stop()
# query_2.stop()
# query_3.stop()


# df_edit_per = df_edit_per_minute \
#     .writeStream \
#     .format("csv")  \
#     .outputMode("append")  \
#     .option("path", f"{args.streaming_bucket}/transformed") \
#     .option("checkpointLocation", f"{args.staging_bucket}/checkpoints/editing_count") \
#     .start()
# df_edit_per.awaitTermination(300)