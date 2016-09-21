# -*- coding: UTF-8 -*-
from spider import SpiderHTML
from multiprocessing import Pool
import sys,urllib,http,random,re,time,datetime
import pymysql
from threading import Timer
pymysql.install_as_MySQLdb()

__author__ = 'waiting'

conn = pymysql.connect(host='localhost',user='root',passwd='',db='test',port=3306,use_unicode=True, charset="utf8")
cur=conn.cursor()
url = "http://www.bilibili.com/"

def run():
    workTime = datetime.datetime.now()
    date = str(workTime).split(" ")[0].replace("-","")
    hour = workTime.hour
    minute = workTime.minute

    msg=""
    try:
        a = SpiderHTML()
        online = a.getUrl(url).find('span',class_='web-online').a.em.string

        args = (online,int(time.time()))
        # print(args)
        cur.execute("INSERT INTO `bili_online`( `online`, `ctime`) VALUES (%s,%s)",args)
        conn.commit()
    except:
        msg = "执行出错"
    finally:
        print("当前时间{0},{1}".format(workTime,msg))    

    #循环定时执行
    global t    #Notice: use global variable!
    t = Timer(300, run)
    t.start()
run()