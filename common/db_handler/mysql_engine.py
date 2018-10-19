#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
# @Time    : 2017/11/14 15:45
# @Author  : HoxHou
# @File    : mysql_engine.py
# @Software: PyCharm Community Edition




import re

import pymysql


class MySQLEngine(object):
    def __init__(self):
        """
        MySQL 数据库ORM
        :param
        """
        self.host = "10.10.13.120"
        self.user = "root"
        self.password = "123456"
        self.charset = "utf8"
        self.db_name = "xhg_testautomation"
        try:
            conn = pymysql.connect(host=self.host, user=self.user, password=self.password,
                                   database=self.db_name, charset=self.charset, connect_timeout=100)
        except pymysql.Error:
            raise
        self.__conn = conn

    def my_execute(self, execute_type, sql):
        """
        :param execute_type:
        :param sql:
        :return:
        """
        try:
            print(sql)  # 后期保存到日志模块
            self.cursor = self.__conn.cursor()
            if execute_type is 'query':
                self.cursor.execute(sql)
                data_list = self.cursor.fetchall()
                table_fields = [each[0] for each in self.cursor.description]
                result=[]
                for row in data_list:
                    obj_dict = {}
                    # 字典键值对
                    for index, value in enumerate(row):
                        obj_dict[table_fields[index]] = value
                    result.append(obj_dict)
                #print(result)  # 后期保存到日志模块
                return result
            elif execute_type in ('insert', 'update', 'delete'):
                try:
                    result={}
                    self.cursor.execute(sql)
                    if execute_type == 'insert':
                        insert_id = self.__conn.insert_id()
                        print('新插入的id：'+str(insert_id))
                        result['insert_id'] = insert_id
                    self.__conn.commit()
                    print("受影响的行：%d" % (self.cursor.rowcount))
                    result['rowcount'] = self.cursor.rowcount
                    return result
                except pymysql.Error:
                    self.__conn.rollback()
                    raise
        finally:
            self.__conn.close()
