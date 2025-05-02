from pyspark.sql import SparkSession
import pyspark.sql.functions as f


spark = SparkSession.master.builder.appName("WikiMedia Streaming").getOrcreate()

df = spark.readStream.format("")