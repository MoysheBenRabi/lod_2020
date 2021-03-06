package com.falcon.core

import java.util

import org.apache.storm.task.ShellBolt
import org.apache.storm.topology.{IRichBolt, OutputFieldsDeclarer}
import org.apache.storm.tuple.Fields


class TaggerBolt() extends ShellBolt("python", "/var/falcon/python/TaggerBolt.py") with IRichBolt {
  override def declareOutputFields(outputFieldsDeclarer: OutputFieldsDeclarer): Unit = {
    outputFieldsDeclarer.declare(new Fields("alarm_tag"))
  }

  override def getComponentConfiguration: util.Map[String, AnyRef] = null
}