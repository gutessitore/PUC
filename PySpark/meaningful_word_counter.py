from pyspark.sql.functions import split, explode, col, lower, regexp_extract
from pyspark.ml.feature import StopWordsRemover
from pyspark.sql import SparkSession
from pandas import DataFrame


def build_spark_session(app_name: str) -> SparkSession:
    """
    Build a SparkSession object.
    :return: SparkSession object
    """
    return SparkSession.builder.appName(app_name).getOrCreate()


def read_text_file(spark: SparkSession, file_name: str) -> DataFrame:
    """
    Read a text file and return a DataFrame.
    :param spark: SparkSession object
    :param file_name: File name
    :return: DataFrame
    """
    return spark.read.text(file_name)


def split_lines(df: DataFrame) -> DataFrame:
    """
    Split lines into words.
    :param df: DataFrame
    :return: DataFrame
    """
    return df.select(split(df.value, " ").alias("line"))


def split_words(df: DataFrame) -> DataFrame:
    """
    Split lines into words.
    :param df: DataFrame
    :return: DataFrame
    """
    return df.select(explode(col("line")).alias("word"))


def lower_words(df: DataFrame) -> DataFrame:
    """
    Lower words.
    :param df: DataFrame
    :return: DataFrame
    """
    return df.select(lower(col("word")).alias("lowered_word"))


def clean_words(df: DataFrame) -> DataFrame:
    """
    Clean words.
    :param df: DataFrame
    :return: DataFrame
    """
    return df.select(regexp_extract(col("lowered_word"), "[a-z]+", 0).alias("cleaned_word"))


def remove_empty_words(df: DataFrame) -> DataFrame:
    """
    Remove empty words.
    :param df: DataFrame
    :return: DataFrame
    """
    return df.filter(col("cleaned_word") != "").select(col("cleaned_word").alias("word"))


def remove_stop_words(df: DataFrame) -> DataFrame:
    """
    Remove stop words.
    :param df: DataFrame
    :return: DataFrame
    """
    stop_words_remover = StopWordsRemover(inputCol="word", outputCol="meaningful")
    words_list_df = df.select(split(col("word"), " ").alias("word"))
    return stop_words_remover.transform(words_list_df).select((col("meaningful")[0]).alias("meaningful"))


def remove_nulls(df: DataFrame) -> DataFrame:
    """
    Remove nulls.
    :param df: DataFrame
    :return: DataFrame
    """
    return df.filter(col("meaningful") != "").where(col("meaningful") != "null")


def count_words(df: DataFrame) -> DataFrame:
    """
    Count words.
    :param df: DataFrame
    :return: DataFrame
    """
    return df.groupBy("meaningful").count().orderBy(col("count").desc())


def meaningful_words_counter(file_name: str) -> DataFrame:
    """
    Count meaningful words.
    :param file_name: File name
    :return: DataFrame
    """
    spark = build_spark_session("Meaningful Words Counter")
    df = read_text_file(spark, file_name)
    df = split_lines(df)
    df = split_words(df)
    df = lower_words(df)
    df = clean_words(df)
    df = remove_empty_words(df)
    df = remove_stop_words(df)
    df = remove_nulls(df)
    df = count_words(df)
    return df


if __name__ == "__main__":
    books_filepath = "books/{}.txt"
    books = [
        books_filepath.format(book_name) for book_name in
        ["frankenstein", "moby-dick", "pride-and-prejudice",
         "the-adventures-of-sherlock-holmes", "the-romance-of-lust"]
    ]

    for book in books:
        meaningful_words = meaningful_words_counter(book)
        print(book)
        meaningful_words.show()
