from pyspark.sql import SparkSession
import pyspark.sql.functions as f

def init_sparksession(staging_bucket,appname="stack-overflow"):
    session =SparkSession.builder.master("yarn").appName(appname).config("temporaryGcsBucket", staging_bucket).getOrCreate()
    return session

def load_sourcetable(session,tablename):
    try:
        table_df = session.read.format("bigquery").option("table", tablename).option("inferSchema", "true")
    except Exception as e:
        print("Tabkle not fount")
        raise
    print(table_df.count(),len(table_df.columns))
    return table_df


def transform_df(df):
    
