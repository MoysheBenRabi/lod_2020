package com.falcon.core

import java.util
import org.apache.storm.spout.ShellSpout
import org.apache.storm.topology.{IRichSpout, OutputFieldsDeclarer}
import org.apache.storm.tuple.Fields

class IPFXSpout() extends ShellSpout("python", "/var/falcon/python/IFXSpoutBolt.py") with IRichSpout {

  override def declareOutputFields(outputFieldsDeclarer: OutputFieldsDeclarer): Unit = {
    outputFieldsDeclarer.declare(new Fields("double", "triple"))
  }

  override def getComponentConfiguration: util.Map[String, AnyRef] = null
}