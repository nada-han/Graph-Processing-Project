from pyspark.sql import SparkSession

def main():
    # Initialiser une session Spark
    spark = SparkSession.builder.appName("GraphXResults").getOrCreate()

    # Chemin des fichiers generes par l'application Scala GraphXApp
    results_path = "/app/data"

    # Charger et afficher les resultats pour chaque index de graphe
    index = 0
    while True:
        try:
            # Chemins des fichiers pour le graphe actuel
            pagerank_file = '{}/graphx_results_{}/pagerank.csv'.format(results_path, index)
            components_file = "{}/graphx_results_{}/connected_components.csv".format(results_path, index)
            triangle_count_file = "{}/graphx_results_{}/triangle_count.csv".format(results_path, index)


            # Charger les donnees dans des DataFrames
            print("--- Resultats pour le Graphe ---", index)
            
            # PageRank
            print("\nPageRank :")
            pagerank_df = spark.read.csv(pagerank_file, schema="vertex STRING, rank DOUBLE", header=False)
            pagerank_df.show()

            # Connected Components
            print("\nComposants Connectes :")
            components_df = spark.read.csv(components_file, schema="vertex STRING, component STRING", header=False)
            components_df.show()

            # Triangle Count
            print("\nCompteur de Triangles :")
            triangle_count_df = spark.read.csv(triangle_count_file, schema="vertex STRING, triangle_count INT", header=False)
            triangle_count_df.show()

            # Passer au graphe suivant
            index += 1
        except Exception as e:
            # Si un fichier manque ou quil ny a plus de resultats
            print("Fin des resultats disponibles ou erreur :",e)
            break

    # Arreter la session Spark
    spark.stop()

if __name__ == "__main__":
    main()