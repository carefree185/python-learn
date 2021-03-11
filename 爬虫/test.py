# import pymysql
#
# db_config = {
#             "host": '127.0.0.1',
#             "port": 3306,
#             'user': 'root',
#             'password': 'dyp1996',
#             'db': 'huya',
#             'charset': 'utf8',
#         }
# connection = pymysql.connect(**db_config)
# cursor = connection.cursor()
# # 创建表需要约定主键为自增长
# # sql = "create table if not exists huya(id int auto_increment primary key, title varchar(255), anchor varchar(255), hot varchar(255));"
# # cursor.execute(sql)
# sql = "insert into huya(title, anchor, hot) values(%s, %s, %s);"
#
# result = cursor.execute(sql, ['哈哈哈', 'xxx', '111'])
# connection.commit()
# print(result)

import logging

# 创建Logger  日志记录
logger = logging.getLogger(name='logger')
logger.setLevel(logging.DEBUG)

# 创建Handler 日志处理, 控制日志显示位置
handler_1 = logging.StreamHandler()  # 控制台显示
handler_2 = logging.FileHandler('test.log')  # 日志输出到文件

# 创建Formatter 日志格式器,控制日志显示格式
formatter = logging.Formatter(fmt='%(asctime)s -- %(name)s -- %(filename)s -- %(levelname)s -- %(message)s')  # 日志格式控制

handler_1.setFormatter(formatter)  # 应用日志格式器到handler对象
handler_2.setFormatter(formatter)

logger.addHandler(handler_1)  # 应用日志处理器到logger对象
logger.addHandler(handler_2)

