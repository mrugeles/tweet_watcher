import sys
import spacy
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import pandas_udf
from pyspark.sql.types import *
from nltk.tokenize import TweetTokenizer

from pyspark.sql.functions import udf
from pyspark.sql.types import ArrayType, StringType


@udf(returnType=ArrayType(StringType()))
def concat_tags(folder, tags):
    return [f"{folder} {tag}" for tag in tags]


if __name__ == "__main__":
    spark = (SparkSession
             .builder
             .appName("TweetJob")
             .getOrCreate())

    spark.udf.register("concat_tags", concat_tags)

    df = (spark.read.format("json")
          .option("inferSchema", "true")
          .load("datasets/"))

    df.createOrReplaceTempView("tweets")

    query = "select " \
            "folder, " \
            "tag, " \
            "count(tag) as count  " \
            "from ( " \
            "select " \
            "explode(concat_tags(folder, HASHTAGS)) as tags, " \
            "split(tags, " ")[0] as folder, " \
            "split(tags, " ")[1] as tag " \
            "from tweets where HASHTAGS is not null) " \
            "group by folder, tag"

    print(spark.sql(query))
