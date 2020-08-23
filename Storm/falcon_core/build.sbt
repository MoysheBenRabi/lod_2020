

name := "falcon_core"

version := "0.1"

scalaVersion := "2.12.12"

scalacOptions += "-Yresolve-term-conflict:package"

enablePlugins(PackPlugin)

// https://mvnrepository.com/artifact/org.apache.storm/storm-core
libraryDependencies += "org.apache.storm" % "storm-core" % "2.2.0" % "${provided.scope}"
libraryDependencies += "org.apache.storm" % "multilang-python" % "2.2.0"
libraryDependencies += "org.apache.storm" % "storm-elasticsearch" % "2.2.0"
libraryDependencies += "org.apache.storm" % "storm-kafka-client" % "2.2.0" % "provided"
libraryDependencies += "org.apache.kafka" % "kafka-clients" % "2.6.0"
