# crawler
# version 0.0.1

FROM mongo

MAINTAINER "tom_giggs" <zamjbn@163.com>

# install Chinese support
# RUN apt -y groupinstall chinese-support
# ENV LANG "zh_CN.UTF-8"

# install something common
RUN apt update
RUN apt install -y gcc gcc+ make libcurl4-openssl-dev libssl-dev git nload curl vim

# install pip
RUN apt-get install -y python2.7 python2.7-dev
RUN apt install -y python
RUN apt install -y python-pip
RUN pip install pip --upgrade
RUN pip install wheel Scrapy scrapy_redis redis pymysql kafka pymongo requests human_curl
#modify mongodb.repo file,make sure the url is valid
RUN apt-get install -y redis-server
RUN apt-get install mysql-server mysql-client