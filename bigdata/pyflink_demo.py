#encoding=utf8
#pip3 install flink
from flink.plan.Environment import get_environment
from flink.functions.GroupReduceFunction import GroupReduceFunction

class Adder(GroupReduceFunction):
    def reduce(self, iterator, collector):
        count, word = iterator.next()
        count += sum([x[0] for x in iterator])
        collector.collect((count, word))


# 1. 获取一个运行环境
env = get_environment()
# 2. 加载/创建初始数据
data = env.from_elements("Who's there?","I think I hear them. Stand, ho! Who's there?")
# 3. 指定对这些数据的操作
data.flat_map(lambda x, c: [(1, word) for word in x.lower().split()]) \
    .group_by(1) \
    .reduce_group(Adder(), combinable=True) \
    .output()
# 4. 运行程序
env.execute(local=True)
#在系统默认python不是python3的时候，需要将pyflink-shell.sh中默认的python版本修改为python3，vi ./pyflink-shell.sh ==>  PYFLINK_PYTHON="${PYFLINK_PYTHON:-"python3"}"

