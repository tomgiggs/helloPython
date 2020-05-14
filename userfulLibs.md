#好用的依赖库
from sh import ls
ls("-l", "/tmp", color="never")
------
import uuid
print(uuid.uuid4())
-------
#一键生成数据报表
pip3 install pandas-profiling

import pandas as pd
import pandas_profiling
data = pd.read_csv(r'E:\dataset\amazon_alexa.tsv',sep="\t")
data.describe()
profile = data.profile_report(title='amazon_alexa Dataset')
profile.to_file(output_file='./amazon_alexa_report.html')
----------
#进度条
pip3 install progressbar
from progressbar import ProgressBar
import time
pbar = ProgressBar(maxval=100)
pbar.start()
for i in range(1, 101):
    pbar.update(i)
    time.sleep(0.1)
pbar.finish()
--------------------------
[binlog2sql 解析mysql的binlog用来还原数据，数据库误操作救急神器](https://github.com/danfengcao/binlog2sql)
--------







