ThisBuild / version := "0.1.0-SNAPSHOT"

ThisBuild / scalaVersion := "2.12.8"

libraryDependencies += "org.apache.spark" %% "spark-core" % "3.5.0"
libraryDependencies += "org.apache.spark" %% "spark-graphx" % "3.5.0"
libraryDependencies += "com.typesafe.play" %% "play-json" % "2.9.4"

lazy val root = (project in file("."))
  .settings(
    name := "Traitement-GraphX"
  )
