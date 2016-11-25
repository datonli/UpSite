
from queue import Queue

q = Queue()
a = [1,2]
q.put(a)

a = [3,4]
q.put(a)
while False == q.empty():
    print('get',q.get())
