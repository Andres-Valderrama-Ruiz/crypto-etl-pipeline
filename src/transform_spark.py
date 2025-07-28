from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, DoubleType

def transform_data(data):
    spark = SparkSession.builder.appName("TransformCoins").getOrCreate()

    cleaned_data = [
        {
            "id": str(d["id"]),
            "name": str(d["name"]),
            "symbol": str(d["symbol"]),
            "current_price": float(d["current_price"]),
            "market_cap": float(d["market_cap"])
        }
        for d in data if all(key in d for key in ["id", "name", "symbol", "current_price", "market_cap"])
    ]

    schema = StructType([
        StructField("id", StringType(), True),
        StructField("name", StringType(), True),
        StructField("symbol", StringType(), True),
        StructField("current_price", DoubleType(), True),
        StructField("market_cap", DoubleType(), True)
    ])

    df = spark.createDataFrame(cleaned_data, schema=schema)
    return df
