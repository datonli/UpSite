# -*- coding: utf-8 -*-

from threading import Thread
from queue import Queue
from time import sleep
#q是任务队列
#NUM是并发线程总数
#JOBS是有多少任务
q = Queue()
NUM = 4
JOBS = 16
#具体的处理函数，负责处理单个任务
def do_somthing_using(arguments):
    print(arguments)
#这个是工作进程，负责不断从队列取数据并处理
def working():
    while True:
        arguments = q.get() #默认队列为空时，线程暂停
        do_somthing_using(arguments)
        sleep(1)
        q.task_done()
#开启线程
threads = []
for i in range(NUM):
    t = Thread(target=working)#线程的执行函数为working
    threads.append(t)
for item in threads:
    item.setDaemon(True)
    item.start()
#JOBS入队
for i in range(JOBS):
    q.put(i)
#等待所有队列为空、再执行别的语句
q.join()
