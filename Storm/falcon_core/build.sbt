name := "falcon_core"

version := "0.1"

scalaVersion := "2.12.12"

scalacOptions += "-Yresolve-term-conflict:package"

enablePlugins(JavaAppPackaging)
enablePlugins(UniversalPlugin)

// https://mvnrepository.com/artifact/org.apache.storm/storm-core
libraryDependencies += "org.apache.storm" % "storm-core" % "2.2.0" % "${provided.scope}"
