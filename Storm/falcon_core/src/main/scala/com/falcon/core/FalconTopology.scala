package com.falcon.core

import org.apache.storm.kafka.spout.FirstPollOffsetStrategy.EARLIEST
import org.apache.kafka.clients.consumer.{ConsumerConfig, ConsumerRecord}
import org.apache.storm.Config
import org.apache.storm.StormSubmitter
import org.apache.storm.kafka.spout.KafkaSpoutRetryExponentialBackoff.TimeInterval
import org.apache.storm.tuple.Fields
import org.apache.storm.tuple.Values
import org.apache.storm.generated.StormTopology
import org.apache.storm.kafka.bolt.KafkaBolt
import org.apache.storm.topology.TopologyBuilder
import org.apache.storm.utils.Utils
import java.util.{Properties, UUID}

import org.apache.storm.kafka.bolt.mapper.FieldNameBasedTupleToKafkaMapper
import org.apache.storm.kafka.bolt.selector.DefaultTopicSelector
import org.apache.storm.elasticsearch.common.EsConfig
import org.apache.storm.elasticsearch.bolt.EsIndexBolt
import org.apache.storm.elasticsearch.common.DefaultEsTupleMapper
import org.apache.storm.kafka.spout.{ByTopicRecordTranslator, KafkaSpout, KafkaSpoutConfig, KafkaSpoutRetryExponentialBackoff}

import scala.collection.mutable

object FalconTopology {
  private val TOPIC_WSH_STREAM = "wsh_stream"
  private val KAFKA_LOCAL_BROKER = "localhost:9092"
  private val ELASTICSEARCH_CLUSTER = "elasticsearch"
  val TOPIC_WSH = "workstation-health"

  @throws[Exception]
  def main(args: Array[String]): Unit = {
    new FalconTopology().runMain(args)
  }
}

class FalconTopology {
  @throws[Exception]
  protected def runMain(args: Array[String]): Unit = {
    val brokerUrl = if (args.length > 0) args(0)
    else FalconTopology.KAFKA_LOCAL_BROKER
    System.out.println("Running with broker url: " + brokerUrl)
    val tpConf = getConfig
    // Получение данных из Kafka. Данные представляют собой стоку с метриками
    StormSubmitter.submitTopology("falcon-topology", tpConf, getTopologyKafkaSpout(getKafkaSpoutConfig(brokerUrl)))
  }

  protected def getConfig: Config = {
    val config = new Config
    config.setDebug(true)
    config
  }

  protected def getTopologyKafkaSpout(spoutConfig: KafkaSpoutConfig[String, String]): StormTopology = {
    val tp = new TopologyBuilder
    val esConfig = new EsConfig(FalconTopology.ELASTICSEARCH_CLUSTER, "localhost:9300")
    // Получение данных
    tp.setSpout("kafka_spout", new KafkaSpout[String, String](spoutConfig), 1)
    // Разметка данных нейросетью
    tp.setBolt("tager_bolt", new TagerBolt).shuffleGrouping("kafka_spout", FalconTopology.TOPIC_WSH_STREAM)
    val tupleMapper = new DefaultEsTupleMapper
    // Сохранение данных в Elasticsearch
    tp.setBolt("es_bolt", new EsIndexBolt(esConfig, tupleMapper))
    tp.createTopology
  }

  protected def getKafkaSpoutConfig(bootstrapServers: String): KafkaSpoutConfig[String, String] = {
    val trans = new ByTopicRecordTranslator[String, String]((r: ConsumerRecord[String,String]) => new Values(r.topic, Integer.valueOf(r.partition), java.lang.Long.valueOf(r.offset), r.key, r.value), new Fields("topic", "partition", "offset", "key", "value"), FalconTopology.TOPIC_WSH_STREAM)
    KafkaSpoutConfig.builder(bootstrapServers, FalconTopology.TOPIC_WSH).setProp(ConsumerConfig.GROUP_ID_CONFIG, "FalconTopologyGroup").setRetry(getRetryService).setRecordTranslator(trans).setOffsetCommitPeriodMs(10000).setFirstPollOffsetStrategy(EARLIEST).setMaxUncommittedOffsets(250).build
  }

  protected def getRetryService = new KafkaSpoutRetryExponentialBackoff(TimeInterval.microSeconds(500), TimeInterval.milliSeconds(2), Integer.MAX_VALUE, TimeInterval.seconds(10))
}