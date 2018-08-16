# -*- coding: utf-8 -*-
# @Time    : 2017/11/21 10:02
# @Author  : Yoson
# @File    : common.py
# @Software: PyCharm


def str_clean(string):
    """清除空格和换行符,把中文逗号，引号换成英文符号"""
    try:
        if string is None:
            string = ''
        else:
            string = str(string)
            string = string.replace(" ", "").replace("\n", "").replace("，", ",").replace("“", "\"").replace("”", "\"")
            string = string.replace("：", ":").replace("’", "\'").replace("\r", "").replace("；", ";").replace("‘", "\'")
        return string
    except Exception:
        print("字符处理出错！！！")






