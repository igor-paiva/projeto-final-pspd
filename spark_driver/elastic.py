from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    explode,
    split,
    length,
    col,
    regexp_replace,
)
from elasticsearch import Elasticsearch
from datetime import datetime


ARTICLES = [
    "a",
    "an",
    "the",
]

CONJUNCTIONS = [
    "for",
    "and",
    "nor",
    "but",
    "or",
    "yet",
    "so",
]

COMMON_PREPOSITIONS = [
    "aboard",
    "about",
    "above",
    "across",
    "after",
    "against",
    "along",
    "amid",
    "among",
    "anti",
    "around",
    "as",
    "at",
    "before",
    "behind",
    "below",
    "beneath",
    "beside",
    "besides",
    "between",
    "beyond",
    "but",
    "by",
    "concerning",
    "considering",
    "despite",
    "down",
    "during",
    "except",
    "excepting",
    "excluding",
    "following",
    "for",
    "from",
    "in",
    "inside",
    "into",
    "like",
    "minus",
    "near",
    "of",
    "off",
    "on",
    "onto",
    "opposite",
    "outside",
    "over",
    "past",
    "per",
    "plus",
    "regarding",
    "round",
    "save",
    "since",
    "than",
    "through",
    "to",
    "toward",
    "towards",
    "under",
    "underneath",
    "unlike",
    "until",
    "up",
    "upon",
    "versus",
    "via",
    "with",
    "within",
    "without",
]

WORDS_TO_FILTER = ARTICLES + CONJUNCTIONS + COMMON_PREPOSITIONS

es = Elasticsearch("http://elasticsearch:9200")

spark = (
    SparkSession.builder.master("spark://spark-master:7077")
    .appName("StreamingWordCountKafkaDistributed")
    .config("spark.driver.host", "spark-driver")
    # .config("spark.driver.port", "5005")
    .config("spark.dynamicAllocation.enabled", "false")
    .config("spark.shuffle.service.enabled", "false")
    .config("spark.streaming.driver.writeAheadLog.closeFileAfterWrite", "true")
    .config("spark.streaming.receiver.writeAheadLog.closeFileAfterWrite", "true")
    .config("spark.executor.memory", "512m")
    .config("spark.executor.instances", "2")
    .config("spark.pyspark.python", "python3")
    .config("spark.pyspark.driver.python", "python3")
    .config("spark.sql.debug.maxToStringFields", "100")
    .getOrCreate()
)

# spark_context = spark.sparkContext
# spark_context.checkpoint("hdfs://hadoop:9000/checkpoint")

lines = (
    spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", "kafka-server:9092")
    .option("failOnDataLoss", "false")
    .option("subscribe", "sentences")
    .option("includeHeaders", "true")
    .option("startingOffsets", "latest")  # we could use earliest
    .option("spark.streaming.kafka.maxRatePerPartition", "50")
    .load()
)

words = (
    lines.select("timestamp", explode(split(lines.value, " ")).alias("word"))
    .withColumn("word", regexp_replace(col("word"), r"[^a-zA-Z'-]", ""))
    .filter(length(col("word")) > 1)
)


def filter_starts_with(word, letter):
    return word.capitalize().startswith(letter)


def filter_by_size(word, length):
    return len(word) == length


def func(batch_df, batch_id):
    print(f"\nBatch ID: {batch_id}")
    print(f"\tReceived words: {batch_df.count()}\n")

    words_list = list(
        filter(
            lambda word: word.lower() not in WORDS_TO_FILTER,
            map(lambda row: row.word, batch_df.collect()),
        )
    )

    print(f"\tFiltered words: {len(words_list)}\n")

    starts_with_s = list(filter(lambda word: filter_starts_with(word, "S"), words_list))
    starts_with_r = list(filter(lambda word: filter_starts_with(word, "R"), words_list))
    starts_with_p = list(filter(lambda word: filter_starts_with(word, "P"), words_list))

    size_6 = list(filter(lambda word: filter_by_size(word, 6), words_list))
    size_8 = list(filter(lambda word: filter_by_size(word, 8), words_list))
    size_11 = list(filter(lambda word: filter_by_size(word, 11), words_list))

    es.index(
        id=batch_id,
        index="words",
        document={
            "words": words_list,
            "total_words": len(words_list),
            "starts_with_s": starts_with_s,
            "starts_with_r": starts_with_r,
            "starts_with_p": starts_with_p,
            "size_6": size_6,
            "size_8": size_8,
            "size_11": size_11,
            "timestamp": datetime.now(),
        },
    )


words.writeStream.foreachBatch(func).start().awaitTermination()
