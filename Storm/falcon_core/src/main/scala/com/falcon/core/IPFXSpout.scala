package com.falcon.core

import java.util

import org.apache.storm.task.ShellBolt
import org.apache.storm.topology.{IRichBolt, OutputFieldsDeclarer}
import org.apache.storm.tuple.Fields

class IPFXSpoutBolt() extends ShellBolt("python", "{absolute path}/splitBoltPython.py") with IRichBolt {
  override def declareOutputFields(outputFieldsDeclarer: OutputFieldsDeclarer): Unit = {
    outputFieldsDeclarer.declare(new Fields("double", "triple"))
  }

  override def getComponentConfiguration: util.Map[String, AnyRef] = null
}