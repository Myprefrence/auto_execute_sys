# -*- coding: utf-8 -*-

# @Time : 2022/2/28 11:20

# @Author : WangJun

# @File : psutil_demo.py

# @Software: PyCharm

import psutil

# 获取CPU信息
print(psutil.cpu_count())  # CPU逻辑数量

psutil.cpu_count(logical=False)  # CPU物理核心

# 2说明是双核超线程, 4则是4核非超线程

# 统计CPU的用户／系统／空闲时间：
psutil.cpu_times()
# scputimes(user=10963.31, nice=0.0, system=5138.67, idle=356102.45)

# 再实现类似top命令的CPU使用率，每秒刷新一次，累计10次：
for x in range(10):
    print(psutil.cpu_percent(interval=1, percpu=True))

#  获取内存信息
# 返回的是字节为单位的整数，可以看到，总内存大小是8589934592 = 8 GB，已用7201386496 = 6.7 GB，使用了66.6%。
# 而交换区大小是1073741824 = 1 GB。
psutil.virtual_memory()
psutil.swap_memory()

# 获取磁盘信息
# 可以通过psutil获取磁盘分区、磁盘使用率和磁盘IO信息
psutil.disk_partitions() # 磁盘分区信息
# [sdiskpart(device='/dev/disk1', mountpoint='/', fstype='hfs', opts='rw,local,rootfs,dovolfs,
# journaled,multilabel')]

psutil.disk_usage('/') # 磁盘使用情况
# sdiskusage(total=998982549504, used=390880133120, free=607840272384, percent=39.1)

psutil.disk_io_counters()  # 磁盘IO
# sdiskio(read_count=988513, write_count=274457, read_bytes=14856830464, write_bytes=17509420032,
# read_time=2228966, write_time=1618405)

# 可以看到，磁盘'/'的总容量是998982549504 = 930 GB，使用了39.1%。文件格式是HFS，opts中包含rw表示可读写，
# journaled表示支持日志。

# 获取网络信息
psutil.net_io_counters() # 获取网络读写字节／包的个数
# snetio(bytes_sent=3885744870, bytes_recv=10357676702, packets_sent=10613069,
#        packets_recv=10423357, errin=0, errout=0, dropin=0, dropout=0)

psutil.net_if_addrs() # 获取网络接口信息

psutil.net_if_stats() # 获取网络接口状态

# 要获取当前网络连接信息，使用net_connections()
psutil.net_connections()

# 获取进程信息
psutil.pids() # 所有进程ID

p = psutil.Process(3776) # 获取指定进程ID=3776，其实就是当前Python交互环境
p.name() # 进程名称
p.exe() # 进程exe路径
p.cwd() # 进程工作目录
p.cmdline() # 进程启动的命令行
p.ppid() # 父进程ID
p.parent() # 父进程
p.children() # 子进程列表
p.status() # 进程状态
p.username() # 进程用户名
p.create_time() # 进程创建时间
p.terminal() # 进程终端
p.cpu_times() # 进程使用的CPU时间
p.memory_info() # 进程使用的内存
p.open_files() # 进程打开的文件
p.connections() # 进程相关网络连接
p.num_threads() # 进程的线程数量
p.threads() # 所有线程信息
p.environ() # 进程环境变量
p.terminate() # 结束进程
# 和获取网络连接类似，获取一个root用户的进程需要root权限，启动Python交互环境或者.py文件时，需要sudo权限

# psutil还提供了一个test()函数，可以模拟出ps命令的效果
psutil.test()
"""
USER         PID %MEM     VSZ     RSS TTY           START    TIME  COMMAND
root           0 24.0 74270628 2016380 ?             Nov18   40:51  kernel_task
root           1  0.1 2494140    9484 ?             Nov18   01:39  launchd
root          44  0.4 2519872   36404 ?             Nov18   02:02  UserEventAgent
root          45    ? 2474032    1516 ?             Nov18   00:14  syslogd
root          47  0.1 2504768    8912 ?             Nov18   00:03  kextd
root          48  0.1 2505544    4720 ?             Nov18   00:19  fseventsd
_appleeven    52  0.1 2499748    5024 ?             Nov18   00:00  appleeventsd
root          53  0.1 2500592    6132 ?             Nov18   00:02  configd
...
"""