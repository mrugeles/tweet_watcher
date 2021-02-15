import sys
import spacy
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import pandas_udf
from pyspark.sql.types import *
from nltk.tokenize import TweetTokenizer


if __name__ == "__main__":
    spark = (SparkSession
             .builder
             .appName("TweetJob")
             .getOrCreate())
    df = (spark.read.format("json")
          .option("inferSchema", "true")
          .load("logs"))

    df.selectExpr("get_tags(text)").show()
