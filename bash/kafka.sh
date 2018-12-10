advertised.listeners=PLAINTEXT://18.191.x.x:9092：从外网无法访问，内网也无法访问


nohup bash kafka-server-start.sh ../config/server.properties >>kafka2.log &


ls -lrt /etc/alternatives/java


cd /data/kafka/kafka_2.12-1.1.0/bin
nohup sudo bash zookeeper-server-start.sh ../config/zookeeper.properties >> /data/zookeeper/zkstart.log &
nohup sudo bash kafka-server-start.sh ../config/server.properties >> /data/kafka/log/kafka_start.log &



export JAVA_HOME=/data/app/jdk8
export KE_HOME=/data/app/kafka-eagle
export PATH=$PATH:$KE_HOME/bin

#查看topic
kafka-topics.sh --zookeeper 127.0.0.1:2181 --list
kafka-topics.sh --zookeeper 127.0.0.1:2181 --topic "ziniao_detail_result" --describe
#查看consumer
kafka-consumer-groups.sh --zookeeper 127.0.0.1:2181 --list
kafka-consumer-groups.sh --zookeeper 127.0.0.1:2181 --group hello_kafka --describe

./kafka-topics.sh -zookeeper localhost:2181 -alter -partitions 4 -topic ziniao_detail_result
#增加kafka的分区数
./kafka-topics.sh -zookeeper localhost:2181 -alter -partitions 4 -topic list_result
#修改kafka的消息保留时间，以小时计算
kafka-configs.sh –zookeeper localhost:2181 –entity-type topics –entity-name test –alter –add-config log.retention.hours=120

#测试kafka的性能
./kafka-producer-perf-test.sh --topic test --num-records 100 --record-size 1 --throughput 100  --producer-props bootstrap.servers=172.31.41.251:9092
#删除kafka的topic
./kafka-topics.sh --zookeeper 127.0.0.1:2181 --delete --topic ziniao_detail_result
#增加jmx查看
vi bin/kafka-run-class.sh  >>> JMX_PORT=8060

#
./kafka-topics.sh --delete --zookeeper 127.0.0.1:2181 --topic asin_cost_calculator


./kafka-console-consumer.sh --bootstrap-server 35.158.x.x:9092 --topic test --from-beginning --new-consumer #新建consumer group
./kafka-consumer-groups.sh --bootstrap-server 35.158.x.x:9092  --list --new-consumer


#获取指定consumer group的位移信息
./kafka-simple-consumer-shell.sh --topic __consumer_offsets --partition 1 --broker-list 35.158.x.x:9092 --formatter "kafka.coordinator.group.GroupMetadataManager\$OffsetsMessageFormatter"

#查询__consumer_offsets topic所有内容
./kafka-console-consumer.sh --topic  __consumer_offsets --bootstrap-server 35.x.x.x:9092 --formatter "kafka.coordinator.group.GroupMetadataManager\$OffsetsMessageFormatter" --consumer.config ../config/consumer.properties --from-beginning


./kafka-consumer-groups.sh --zookeeper 127.0.0.1:2181 --list #仅仅显示zookeeper里面注册的consumer，不显示Java consumer API的用户组
./kafka-consumer-groups.sh --new-consumer --bootstrap-server 35.x.x.x:9092 --list #显示活跃consumer消费者组
./kafka-consumer-groups.sh --new-consumer --bootstrap-server 127.0.0.1:9092 --group s3_uploader --describe #consumer 消费者消费详情
./kafka-run-class.sh kafka.tools.ConsumerOffsetChecker --zookeeper 127.0.0.1:2181 --group s3_uploader


SELECT count(*) FROM "ziniao_detail_result" WHERE "partition" IN (2) 


http://35.158.103.147:8048/ke/topic/message



#磁盘开机自动挂载方法：
成功挂载后，修改/etc/fstab使之开机自动挂载，添加以下内容

/dev/sdb                /data                   ext4    defaults        0 0
lsblk /dev/xvdg