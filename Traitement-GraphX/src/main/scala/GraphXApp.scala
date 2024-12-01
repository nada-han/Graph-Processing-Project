import org.apache.spark.{SparkConf, SparkContext}
import org.apache.spark.graphx.{Edge, Graph}
import play.api.libs.json._
import java.io.PrintWriter

object GraphXApp {
  def main(args: Array[String]): Unit = {
    // Configure Spark
    val conf = new SparkConf().setAppName("GraphXApp").setMaster("local[*]")
    val sc = new SparkContext(conf)

    // Fetch graph data from API
    val apiUrl = "http://127.0.0.1:5000/graph"
    val graphData = scala.io.Source.fromURL(apiUrl).mkString

    // Parse JSON
    val json = Json.parse(graphData)
    val edgesList = (json \\ "edges").map { edge =>
      val src = (edge \ "src").as[Long]
      val dst = (edge \ "dst").as[Long]
      Edge(src, dst, 1.0) // Weight is optional
    }

    // Create graph
    val edges = sc.parallelize(edgesList)
    val vertices = edges.flatMap(edge => Seq((edge.srcId, edge.srcId), (edge.dstId, edge.dstId))).distinct()
    val graph = Graph(vertices, edges)

    // Apply GraphX algorithms
    val resultsPath = "/tmp/graphx_results"

    // 1. PageRank
    val pagerank = graph.pageRank(0.15).vertices.collect()
    saveResults(resultsPath + "/pagerank.csv", pagerank.map { case (id, rank) => s"$id,$rank" })

    // 2. Connected Components
    val components = graph.connectedComponents().vertices.collect()
    saveResults(resultsPath + "/connected_components.csv", components.map { case (id, component) => s"$id,$component" })

    // 3. Triangle Counting
    val triangleCounts = graph.triangleCount().vertices.collect()
    saveResults(resultsPath + "/triangle_count.csv", triangleCounts.map { case (id, count) => s"$id,$count" })

    // Stop SparkContext
    sc.stop()
  }

  // Helper function to save results to file
  def saveResults(filePath: String, results: Array[String]): Unit = {
    val writer = new PrintWriter(filePath)
    results.foreach(writer.println)
    writer.close()
  }
}