from pyspark import SparkConf
from pyspark.sql import SparkSession
import os
from pyspark.sql.functions import lit

def process_graph_results(graph_name, results_folder, spark, neo4j_options):
    # Define paths for each algorithm's results based on the graph's name
    pagerank_path = os.path.join(results_folder, f"{graph_name}/pagerank.csv")
    components_path = os.path.join(results_folder, f"{graph_name}/connected_components.csv")
    triangle_count_path = os.path.join(results_folder, f"{graph_name}/triangle_count.csv")

    # Reading CSV files into DataFrames for each algorithm's result
    pagerank_df = spark.read.option("header", "false").csv(pagerank_path).toDF("id", "pagerank")
    components_df = spark.read.option("header", "false").csv(components_path).toDF("id", "component")
    triangle_count_df = spark.read.option("header", "false").csv(triangle_count_path).toDF("id", "triangle_count")

    # Add a graph-specific identifier to distinguish nodes
    pagerank_df = pagerank_df.withColumn("graph_name", lit(graph_name))
    components_df = components_df.withColumn("graph_name", lit(graph_name))
    triangle_count_df = triangle_count_df.withColumn("graph_name", lit(graph_name))

    # Insert results into Neo4j for each algorithm
    print(f"Inserting PageRank results for graph {graph_name} into Neo4j...")
    pagerank_df.write \
        .format("org.neo4j.spark.DataSource") \
        .mode("append") \
        .option("labels", ":Vertex") \
        .option("node.keys", "id,graph_name") \
        .options(**neo4j_options) \
        .save()

    print(f"Inserting Connected Components results for graph {graph_name} into Neo4j...")
    components_df.write \
        .format("org.neo4j.spark.DataSource") \
        .mode("append") \
        .option("labels", ":Vertex") \
        .option("node.keys", "id,graph_name") \
        .options(**neo4j_options) \
        .save()

    print(f"Inserting Triangle Count results for graph {graph_name} into Neo4j...")
    triangle_count_df.write \
        .format("org.neo4j.spark.DataSource") \
        .mode("append") \
        .option("labels", ":Vertex") \
        .option("node.keys", "id,graph_name") \
        .options(**neo4j_options) \
        .save()

    print(f"All results for graph {graph_name} have been successfully inserted into Neo4j.")


def main():
    # Configuration for Spark with the Neo4j connector
    conf = (
        SparkConf()
        .setAppName("GraphXApp")
        .setMaster("local[*]")
        .set("spark.jars.packages", "org.neo4j:neo4j-connector-apache-spark_2.12:5.3.2_for_spark_3")
    )
    spark = SparkSession.builder.config(conf=conf).getOrCreate()

    # Path to the results folder containing the subdirectories for each graph
    results_folder = "/app/data"

    # Neo4j connection parameters
    neo4j_uri = "bolt://neo4j:7687"
    neo4j_user = "neo4j"  # Replace with your username
    neo4j_password = "password"  # Replace with your password
    neo4j_options = {
        "url": neo4j_uri,
        "authentication.basic.username": neo4j_user,
        "authentication.basic.password": neo4j_password,
    }

    # Get a list of all graph directories
    graph_names = [name for name in os.listdir(results_folder) if os.path.isdir(os.path.join(results_folder, name))]

    # Process each graph and insert the results into Neo4j
    for graph_name in graph_names:
        print(f"Processing graph: {graph_name}")
        process_graph_results(graph_name, results_folder, spark, neo4j_options)

    # Stop Spark
    spark.stop()

if __name__ == "__main__":
    main()
