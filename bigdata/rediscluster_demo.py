#encoding=utf8
# import redis.Redis
from  rediscluster.client import StrictRedisCluster
# from rediscluster.client
nodes = [{'host':'114.116.43.125','port':9001}, {'host':'114.116.43.125','port':9002},
                                                   {'host': '114.116.43.125', 'port': 9003},{'host':'114.116.43.125','port':9004},
                                                   {'host': '114.116.43.125', 'port': 9005},{'host':'114.116.43.125','port':9006}]
cluster_client = StrictRedisCluster(startup_nodes=nodes,
                                    max_connections=20,skip_full_coverage_check=True,)
#建立连接好缓慢啊，几乎要四五分钟,节点可以填一两个就行，没全部填进入也没事,慢是因为集群配置有问题吗,这个库会缓存所有的集群槽，
# 一直在nodemanage.py里面的initialize 中循环循环（212行）,在内网测试就非常快，所以这个没有多大的问题
tmp = cluster_client.get('zillo')
print(tmp)
print(cluster_client.cluster_info())
'''
Json.cn
在线解析 什么是JSON JSON解析代码 JSON组件


{"172.16.0.71:9001": {"cluster_stats_messages_pong_sent": 337918, "cluster_stats_messages_meet_received": 5, "cluster_state": "ok", "cluster_slots_assigned": 16384, "cluster_known_nodes": 6, "cluster_stats_messages_pong_received": 332547, "cluster_slots_fail": 0, "cluster_stats_messages_received": 670465, "cluster_stats_messages_ping_sent": 332547, "cluster_stats_messages_ping_received": 337913, "cluster_size": 3, "cluster_current_epoch": 6, "cluster_stats_messages_sent": 670465, "cluster_slots_pfail": 0, "cluster_my_epoch": 1, "cluster_slots_ok": 16384}, "172.16.0.71:9002": {"cluster_stats_messages_pong_sent": 327570, "cluster_stats_messages_meet_received": 2, "cluster_state": "ok", "cluster_slots_assigned": 16384, "cluster_stats_messages_meet_sent": 3, "cluster_known_nodes": 6, "cluster_stats_messages_pong_received": 332304, "cluster_slots_fail": 0, "cluster_stats_messages_received": 659874, "cluster_stats_messages_ping_sent": 332301, "cluster_stats_messages_ping_received": 327568, "cluster_size": 3, "cluster_current_epoch": 6, "cluster_stats_messages_sent": 659874, "cluster_slots_pfail": 0, "cluster_my_epoch": 2, "cluster_slots_ok": 16384}, "172.16.0.71:9003": {"cluster_stats_messages_pong_sent": 335109, "cluster_stats_messages_meet_received": 2, "cluster_state": "ok", "cluster_slots_assigned": 16384, "cluster_stats_messages_meet_sent": 4, "cluster_known_nodes": 6, "cluster_stats_messages_pong_received": 332674, "cluster_slots_fail": 0, "cluster_stats_messages_received": 667783, "cluster_stats_messages_ping_sent": 332670, "cluster_stats_messages_ping_received": 335107, "cluster_size": 3, "cluster_current_epoch": 6, "cluster_stats_messages_sent": 667783, "cluster_slots_pfail": 0, "cluster_my_epoch": 3, "cluster_slots_ok": 16384}, "172.16.0.71:9004": {"cluster_stats_messages_pong_sent": 330755, "cluster_stats_messages_meet_received": 2, "cluster_state": "ok", "cluster_slots_assigned": 16384, "cluster_stats_messages_meet_sent": 4, "cluster_known_nodes": 6, "cluster_stats_messages_pong_received": 332622, "cluster_slots_fail": 0, "cluster_stats_messages_received": 663377, "cluster_stats_messages_ping_sent": 332618, "cluster_stats_messages_ping_received": 330753, "cluster_size": 3, "cluster_current_epoch": 6, "cluster_stats_messages_sent": 663377, "cluster_slots_pfail": 0, "cluster_my_epoch": 2, "cluster_slots_ok": 16384}, "172.16.0.71:9005": {"cluster_stats_messages_pong_sent": 340213, "cluster_stats_messages_meet_received": 4, "cluster_state": "ok", "cluster_slots_assigned": 16384, "cluster_stats_messages_meet_sent": 1, "cluster_known_nodes": 6, "cluster_stats_messages_pong_received": 332575, "cluster_slots_fail": 0, "cluster_stats_messages_received": 672788, "cluster_stats_messages_ping_sent": 332574, "cluster_stats_messages_ping_received": 340209, "cluster_size": 3, "cluster_current_epoch": 6, "cluster_stats_messages_sent": 672788, "cluster_slots_pfail": 0, "cluster_my_epoch": 3, "cluster_slots_ok": 16384}, "172.16.0.71:9006": {"cluster_stats_messages_pong_sent": 323682, "cluster_stats_messages_meet_received": 2, "cluster_state": "ok", "cluster_slots_assigned": 16384, "cluster_stats_messages_meet_sent": 5, "cluster_known_nodes": 6, "cluster_stats_messages_pong_received": 332525, "cluster_slots_fail": 0, "cluster_stats_messages_received": 656207, "cluster_stats_messages_ping_sent": 332520, "cluster_stats_messages_ping_received": 323680, "cluster_size": 3, "cluster_current_epoch": 6, "cluster_stats_messages_sent": 656207, "cluster_slots_pfail": 0, "cluster_my_epoch": 1, "cluster_slots_ok": 16384}}
      
{
    "172.16.0.71:9001":{
        "cluster_stats_messages_pong_sent":337918,
        "cluster_stats_messages_meet_received":5,
        "cluster_state":"ok",
        "cluster_slots_assigned":16384,
        "cluster_known_nodes":6,
        "cluster_stats_messages_pong_received":332547,
        "cluster_slots_fail":0,
        "cluster_stats_messages_received":670465,
        "cluster_stats_messages_ping_sent":332547,
        "cluster_stats_messages_ping_received":337913,
        "cluster_size":3,
        "cluster_current_epoch":6,
        "cluster_stats_messages_sent":670465,
        "cluster_slots_pfail":0,
        "cluster_my_epoch":1,
        "cluster_slots_ok":16384
    },
    "172.16.0.71:9002":{
        "cluster_stats_messages_pong_sent":327570,
        "cluster_stats_messages_meet_received":2,
        "cluster_state":"ok",
        "cluster_slots_assigned":16384,
        "cluster_stats_messages_meet_sent":3,
        "cluster_known_nodes":6,
        "cluster_stats_messages_pong_received":332304,
        "cluster_slots_fail":0,
        "cluster_stats_messages_received":659874,
        "cluster_stats_messages_ping_sent":332301,
        "cluster_stats_messages_ping_received":327568,
        "cluster_size":3,
        "cluster_current_epoch":6,
        "cluster_stats_messages_sent":659874,
        "cluster_slots_pfail":0,
        "cluster_my_epoch":2,
        "cluster_slots_ok":16384
    },
    "172.16.0.71:9003":{
        "cluster_stats_messages_pong_sent":335109,
        "cluster_stats_messages_meet_received":2,
        "cluster_state":"ok",
        "cluster_slots_assigned":16384,
        "cluster_stats_messages_meet_sent":4,
        "cluster_known_nodes":6,
        "cluster_stats_messages_pong_received":332674,
        "cluster_slots_fail":0,
        "cluster_stats_messages_received":667783,
        "cluster_stats_messages_ping_sent":332670,
        "cluster_stats_messages_ping_received":335107,
        "cluster_size":3,
        "cluster_current_epoch":6,
        "cluster_stats_messages_sent":667783,
        "cluster_slots_pfail":0,
        "cluster_my_epoch":3,
        "cluster_slots_ok":16384
    },
    "172.16.0.71:9004":{
        "cluster_stats_messages_pong_sent":330755,
        "cluster_stats_messages_meet_received":2,
        "cluster_state":"ok",
        "cluster_slots_assigned":16384,
        "cluster_stats_messages_meet_sent":4,
        "cluster_known_nodes":6,
        "cluster_stats_messages_pong_received":332622,
        "cluster_slots_fail":0,
        "cluster_stats_messages_received":663377,
        "cluster_stats_messages_ping_sent":332618,
        "cluster_stats_messages_ping_received":330753,
        "cluster_size":3,
        "cluster_current_epoch":6,
        "cluster_stats_messages_sent":663377,
        "cluster_slots_pfail":0,
        "cluster_my_epoch":2,
        "cluster_slots_ok":16384
    },
    "172.16.0.71:9005":{
        "cluster_stats_messages_pong_sent":340213,
        "cluster_stats_messages_meet_received":4,
        "cluster_state":"ok",
        "cluster_slots_assigned":16384,
        "cluster_stats_messages_meet_sent":1,
        "cluster_known_nodes":6,
        "cluster_stats_messages_pong_received":332575,
        "cluster_slots_fail":0,
        "cluster_stats_messages_received":672788,
        "cluster_stats_messages_ping_sent":332574,
        "cluster_stats_messages_ping_received":340209,
        "cluster_size":3,
        "cluster_current_epoch":6,
        "cluster_stats_messages_sent":672788,
        "cluster_slots_pfail":0,
        "cluster_my_epoch":3,
        "cluster_slots_ok":16384
    },
    "172.16.0.71:9006":{
        "cluster_stats_messages_pong_sent":323682,
        "cluster_stats_messages_meet_received":2,
        "cluster_state":"ok",
        "cluster_slots_assigned":16384,
        "cluster_stats_messages_meet_sent":5,
        "cluster_known_nodes":6,
        "cluster_stats_messages_pong_received":332525,
        "cluster_slots_fail":0,
        "cluster_stats_messages_received":656207,
        "cluster_stats_messages_ping_sent":332520,
        "cluster_stats_messages_ping_received":323680,
        "cluster_size":3,
        "cluster_current_epoch":6,
        "cluster_stats_messages_sent":656207,
        "cluster_slots_pfail":0,
        "cluster_my_epoch":1,
        "cluster_slots_ok":16384
    }
}


'''
print(cluster_client.cluster_nodes())
