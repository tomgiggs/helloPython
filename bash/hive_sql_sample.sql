Create [EXTERNAL] TABLE [IF NOT EXISTS] table_name
 [(col_name data_type [COMMENT col_comment], ...)]
 [COMMENT table_comment]
 [PARTITIONED BY (col_name data_type [COMMENT col_comment], ...)]
 [CLUSTERED BY (col_name, col_name, ...) [SORTED BY (col_name [ASC|DESC], ...)]INTO num_buckets BUCKETS]
 [ROW FORMAT row_format]
 [STORED AS file_format]
 [LOCATION hdfs_path]


#根据json文件创建表
CREATE EXTERNAL TABLE `t_product_list_json_test`(
  `nodeid` string COMMENT 'from deserializer',
  `asin` string COMMENT 'from deserializer',
  `review_num` string COMMENT 'from deserializer',
  `img_src` string COMMENT 'from deserializer',
  `price` string COMMENT 'from deserializer',
  `is_prime` string COMMENT 'from deserializer',
  `title` string COMMENT 'from deserializer',
  `star` string COMMENT 'from deserializer',
  `country` string COMMENT 'from deserializer')
 PARTITIONED BY (
  `country` string,
  `month` int,
  day int)
ROW FORMAT SERDE
  'org.openx.data.jsonserde.JsonSerDe'
WITH SERDEPROPERTIES (
  'ignore.malformed.json'='true')
STORED AS INPUTFORMAT
  'org.apache.hadoop.mapred.TextInputFormat'
OUTPUTFORMAT
  'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION
  's3://bucket/path to file/'


#创建orc表
CREATE EXTERNAL TABLE `product_orc`(
  `id` bigint COMMENT 'id',
  `asin` string COMMENT 'asin',
  `star` float,
  `offer_num` int,
  `brand_name` string,
  `rank_html` string)
PARTITIONED BY (
  `country` string)
ROW FORMAT SERDE
  'org.apache.hadoop.hive.ql.io.orc.OrcSerde'
STORED AS INPUTFORMAT
  'org.apache.hadoop.hive.ql.io.orc.OrcInputFormat'
OUTPUTFORMAT
  'org.apache.hadoop.hive.ql.io.orc.OrcOutputFormat'
LOCATION
  's3://bucket/path to orc file'
TBLPROPERTIES (
  'transient_lastDdlTime'='1526039830')

#创建分区分桶表
CREATE EXTERNAL TABLE `yr_sl_as_ord`(
  `weekend_day` string,
  `seller_id` string,
  `asin` string,
  `gross_units` int,
  `fba_units` int
PARTITIONED BY (
  `country` string,
  `dt` string)
CLUSTERED BY (
  asin)
INTO 10 BUCKETS
ROW FORMAT SERDE
  'org.apache.hadoop.hive.ql.io.orc.OrcSerde'
STORED AS INPUTFORMAT
  'org.apache.hadoop.hive.ql.io.orc.OrcInputFormat'
OUTPUTFORMAT
  'org.apache.hadoop.hive.ql.io.orc.OrcOutputFormat'
LOCATION
  's3://bucket/path to orc file'
TBLPROPERTIES (
  'transient_lastDdlTime'='1526039890')
#新建分区并添加数据，注意最后的文件夹名称是分区=xxx
 alter table product_orc add if not exists partition(country='us') location "s3://bucket/path to orc file/country=us";

alter table yr_sl_as_ord add partition(country='us',dt='2017') location"s3://bucket/path to orc file/country=us/dt=2017";

#根据查询结果创建表
create table  query_result  as
select (t1.asin ,gross_units,gross_amount,product_name, star, offer_num, brand_name, fba, amazon, release_date)
 from (select asin,sum(giftwrap_amount) as giftwrap_amount, 'us' as country, '2017' as dt , seller_id , weekend_day  from xxx where (country='us'and dt='2017' ) group by asin, seller_id,weekend_day ) t1 left join (select * from product_xxx  where country='us') t2 on t1.asin =  t2.asin ;
#根据查询结果创建外部表
create external table asin_seller
LOCATION 's3://bucket/tmp/hive_asin'
 as
select asin,collect_set(seller_id) from ***  group  by asin

CREATE TABLE associate_mx_2017 (
  store_cnt int,
  weekend_day string,
  is_weekend tinyint,
  ordered_units int ,
  asin string ,
  country string
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES(
"separatorChar"=",","quoteChar"= "'","escapeChar"="\\"
)
STORED AS TEXTFILE;


CREATE TABLE associate_test (
  store_cnt int,
  weekend_day string,
  is_weekend tinyint,
  ordered_units int ,
  ordered_amt double ,
  asin string ,
  country string
)
ROW FORMAT DELIMITED
   FIELDS TERMINATED BY ','
 STORED AS TEXTFILE;

#hive 相关配置
classification=yarn-site,properties=[yarn.nodemanager.resource.memory-mb=18000]
set hive.tez.container.size=4096;
set hive.tez.auto.reducer.parallelism=true;
set tez.am.container.reuse.enabled=true;
set hive.exec.dynamic.partition.mode=nonstrict;
set hive.exec.max.dynamic.partitions.pernode = 500;
set hive.exec.max.dynamic.partitions = 3000;
set hive.tez.auto.reducer.parallelism=true;


##############################################################################



CREATE TABLE `associate_us_2017`(
  `store_cnt` bigint,
  `weekend_day` string,
  `is_weekend` string,
  `glance_view_count` bigint,
  `ordered_units` bigint,
  `ordered_prod_sales_amt` double,
  `customers` bigint,
  `new_customers` bigint,
  `asin` string,
  `associate_segment_id` string,
  `traffic_channel_id` string,
  `country` string)
ROW FORMAT SERDE
  'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'
STORED AS INPUTFORMAT
  'org.apache.hadoop.mapred.TextInputFormat'
OUTPUTFORMAT
  'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION
  's3://bucket/tmp/hive_result'
TBLPROPERTIES (
  'transient_lastDdlTime'='1526364710')



sqoop export --connect jdbc:mysql://XXX:11016/product001?charset=utf8 --username 'rootx' --password 'xxxx' --table 'associate_us_2017'  --hcatalog-table 'query_result_associate'

sqoop export --connect jdbc:mysql://xxxxxx:11016/product001?charset=utf8 --username 'rootx' --password 'xxxx' --table 'associate_us_2017'  --export-dir 's3://bucket/tmp/hive_result'

 insert overwrite directory "s3://bucket/tmp/table_name" row format delimited fields terminated by',' select * from query_result_associate ;

 insert overwrite localdirectory '/home/hadoop/export_hive' row format delimited fields terminated by '\t' collection items terminated by ',' map keys terminated by ':' select * from userinfo;






  CREATE EXTERNAL TABLE `au_detail_test`(
  `id` int, 
  `product_id` string, 
  `asin` string, 
  `marketplace_id` string, 
  `rank` int, 
  `reviews` int, 
  `product_url` string, 
  `img_url` string, 
  `buy_box_price` float, 
  `buy_box` string, 
  `product_name` string,
  `offer_num` int, 
  `brand_name` string, 
  `amazon_choice` string)
ROW FORMAT SERDE 
  'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe' 
STORED AS INPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat' 
OUTPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat'
LOCATION
  's3://bucket/product_detail/au'
TBLPROPERTIES (
  'transient_lastDdlTime'='1526612463')



CREATE EXTERNAL TABLE `detail_de`(
  `asin` string,
  `product_name` string,
  `star` float, 
  `rank_html` string,
  `category_text` string, 
  `offer_num` int, 
  `brand_name` string
)
ROW FORMAT SERDE 
  'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe' 
WITH SERDEPROPERTIES ( 
  'path'='s3://bucket/product_detail/de')
STORED AS INPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat' 
OUTPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat'
LOCATION
  's3://bucket/product_detail/de'
TBLPROPERTIES (
  'spark.sql.create.version'='2.3.0', 
  'spark.sql.sources.provider'='parquet', 
  'spark.sql.sources.schema.numParts'='1', 
  'spark.sql.sources.schema.part.0'='{\"type\":\"struct\",\"fields\":[{\"name\":\"asin\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"brand_name\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}}]}',
  'transient_lastDdlTime'='1526630425')

MSCK REPAIR TABLE t_product_list_json_all_2018;

 create  table product_detail_au_simple
[stored as orc]
 location
    's3://bucket/hive_data/product_detail/au'
 as
 select b.* from (select a.asin, a.rank, a.reviews, a.buy_box_price, a.buy_box, a.product_name, a.star from (select *, row_number() over (partition by country,asin  order by  create_time  desc) rid from  product_detail.detail_au  ) as a where a.rid=1 )  as b



#增量更新表记录
 insert overwrite table product_detail.detail_au
 select  id ,product_id ,asin ,marketplace_id ,rank,reviews,product_url ,img_url,brand_name ,fba,amazon,feature ,description ,release_date ,create_time ,craw_time ,seller_id ,sold_by  FROM  select * from (select *, row_number() over (partition by country,asin  order by  create_time  desc) rid from  product_detail.detail_au  ) where a.rid=1
insert overwrite table product_detail.detail_ca
select * from (select *, row_number() over (partition by country,asin  order by  create_time  desc) rid from  detail_au  ) where rid=1;



CREATE EXTERNAL TABLE `cfg_asin_category_test3`(
  `asin` string,
  `gl_product_group` string,
  `category_code` string,
  `subcategory_code` string,
  `country` string)
LOCATION
  's3://datacubes/hive_data/test'

ROW FORMAT DELIMITED
  FIELDS TERMINATED BY ','  enclosed by '\"'
STORED AS INPUTFORMAT
  'org.apache.hadoop.mapred.TextInputFormat'
OUTPUTFORMAT
  'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION
  's3://datacubes/hive_data/test'




UPDATE t_cate_seller  t  LEFT JOIN  t_seller_name_au p ON t.seller_id=p.seller_id SET t.seller_name=p.seller_name where t.seller_name='';

create TABLE `t_glance_view_count` like sample;
create TABLE `t_selection_` like selection_sample;

ALTER TABLE `associate` RENAME t_associate_au_2017;

ALTER TABLE  `associate_au` ADD INDEX `index_asin` (ASIN);

SELECT ASIN FROM t_product_detail_au_new INTO OUTFILE"/data/au_crawled.txt";

REPLACE INTO  t_product_detai SELECT * FROM `t_product_detail_us_01` WHERE create_time >'2018-04-25 00:00:00';

create table t_product_review like review_sample ;

SELECT ASIN FROM  `t_product_detail`  WHERE reviews >10 INTO OUTFILE "/data/review_asin_00.txt";

./sqoop import --append --connect jdbc:oracle:thin:@192.168.1.101:1521:orcl --username sun --password sun --target-dir /clxx_parquet  --num-mappers 1 --table x_clxx --columns clxxbh,kkbh,jksbbh,jgsj,jgsk,xsfx,cdbh,hphm,hpys --as-parquetfile ;


insert overwrite directory "s3://bucket/tmp/asin_result" row format delimited fields terminated by'\t' collection items terminated by ','  select * from asin_seller ;

#
SELECT count(*)
FROM
    (SELECT asin
    FROM ziniao_productxxx
    WHERE country='jp'
            AND dt='12'group by asin ) t LEFT outer
JOIN
    (SELECT asin
    FROM t_product_cost_xxx
    WHERE country='jp'
    GROUP BY  asin ) b
    ON t.asin=b.asin  where b.asin is null



select main_asin from (select main_asin,array_join( transform(data,x -> json_extract_scalar(json_parse(x),'$.img') ),',','' )as img from t_product_asin_sponsor_test01 ) where strpos(img,'/gp/sponsored-products')>0

select father_url, regexp_extract_all(father_id, '/\d+') as father_id, father_cate_name, category_url, category_level, node_id, node_name, craw_time, country, date from  t_product_release_category;

select father_url, array_join(regexp_extract_all(father_id, '/\d+'),'','' )as father_id, father_cate_name, category_url, category_level, node_id, node_name, craw_time, country, date from  t_product_release_category;
