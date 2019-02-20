# administrative_region
行政区域查询接口

#python3.5.2

接口设计思想
主要分为2部分：
    1、爬去行政区划分的数据源存入到mongo数据库
    2、根据参数从接口获取相应的数据

实现：
    1、使用tornado框架搭建，利用aiohttp库实现爬取数据，然后根据区域编号分为3层进行存储
    2、url传参必须要有区域编号或者省级行政区域的名称关键字
    3、第一次请求会进行数据爬取，存入mongo再返回，后面的请求直接从mongo拿

运行：
    1、自行下载mongodb
    2、将mongod命令配置到环境变量
    3、bash db_start
    4、pip安装需要的包
    5、run start.py