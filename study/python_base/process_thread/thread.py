# -*- coding: utf-8 -*-

# @Time : 2022/2/25 16:20

# @Author : WangJun

# @File : thread.py

# @Software: PyCharm

# Python的标准库提供了两个模块：_thread和threading，_thread是低级模块，threading是高级模块，
# 对_thread进行了封装。绝大多数情况下，我们只需要使用threading这个高级模块。
#
# 启动一个线程就是把一个函数传入并创建Thread实例，然后调用start()开始执行

import time, threading

# 新线程执行的代码:
def loop():
    print('thread %s is running...' % threading.current_thread().name)
    n = 0
    while n < 5:
        n = n+1
        print('thread %s >>> %s' % (threading.current_thread().name, n))
        time.sleep(1)

    print('thread %s ended.' % threading.current_thread().name)

print('thread %s is running...' % threading.current_thread().name)
t = threading.Thread(target=loop, name='LoopThread')
t.start()
t.join()
print('thread %s ended.' % threading.current_thread().name)


from concurrent.futures import ThreadPoolExecutor

def test(value1, value2=None):
    print("%s threading is printed %s, %s" % (threading.current_thread().name, value1, value2))
    time.sleep(2)
    return 'finished'

def test_result(future):
    print(future.result())


if __name__ == "__main__":
    # 如果程序不希望直接调用 result() 方法阻塞线程，则可通过 Future 的 add_done_callback()
    # 方法来添加回调函数，该回调函数形如 fn(future)。当线程任务完成后，程序会自动触发该回调函数，
    # 并将对应的 Future 对象作为参数传给该回调函数
    import numpy as np
    threadPool = ThreadPoolExecutor(max_workers=4, thread_name_prefix="test_")
    for i in range(0, 10):
        future = threadPool.submit(test, i, i+1)
        future.add_done_callback(test_result)
        # print(future.result())

    threadPool.shutdown(wait=True)
    print('main finished')