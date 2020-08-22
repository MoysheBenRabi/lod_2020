package com.falcon.core

import org.apache.storm.{Config, LocalCluster, StormSubmitter}
import org.apache.storm.topology.TopologyBuilder
import org.apache.storm.tuple.Fields

/**
 * Created by gkatzioura on 2/18/17.
 */
object FalconTopology  {

  def main(args: Array[String]): Unit = {
    println("Hello, world!")
    val builder = new TopologyBuilder


    val conf = new Config()
    conf.setDebug(true)

    if (args != null && args.length > 0) {
      conf.setNumWorkers(3)
      StormSubmitter.submitTopology(args(0), conf, builder.createTopology())
    }
    else {
      conf.setMaxTaskParallelism(3)
      val cluster = new LocalCluster
      cluster.submitTopology("word-count", conf, builder.createTopology())
      Thread.sleep(10000)
      cluster.shutdown()
    }
  }
}