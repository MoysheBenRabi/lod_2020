package com.falcon.core

import java.text.BreakIterator

import org.apache.storm.topology. {
  BasicOutputCollector,
  OutputFieldsDeclarer
}
import org.apache.storm.topology.base.BaseBasicBolt
import org.apache.storm.tuple. {
  Fields,
  Tuple,
  Values
} /** * Created by gkatzioura on 2/18/17. */
class TaggerBolt extends BaseBasicBolt {
  override def execute(input: Tuple, collector: BasicOutputCollector): Unit = {
  }

  override def declareOutputFields(declarer: OutputFieldsDeclarer): Unit = {
    declarer.declare(new Fields("alarm_tag"))
  }
}



