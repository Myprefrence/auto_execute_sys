# -*- coding: utf-8 -*-

# @Time : 2022/2/25 15:02

# @Author : WangJun

# @File : opreation_dir_file.py

# @Software: PyCharm

import os

print(os.name)  # 操作系统类型
# 如果是posix，说明系统是Linux、Unix或Mac OS X，如果是nt，就是Windows系统。
# 要获取详细的系统信息，可以调用uname()函数
print(os.uname())

# 环境变量
# 在操作系统中定义的环境变量，全部保存在os.environ这个变量中，可以直接查看
print(os.environ)

# 要获取某个环境变量的值，可以调用os.environ.get('key')
print(os.environ.get('path'))

# 操作文件和目录
# 操作文件和目录的函数一部分放在os模块中，一部分放在os.path模块中，这一点要注意一下。
# 查看、创建和删除目录可以这么调用：

# 查看当前目录的绝对路径:
print(os.path.abspath('.'))

# 在某个目录下创建一个新目录，首先把新目录的完整路径表示出来:
os.path.join('/Users/michael', 'testdir')

# 然后创建一个目录:
os.mkdir('/Users/michael/testdir')

# 删掉一个目录:
os.rmdir('/Users/michael/testdir')

# 同样的道理，要拆分路径时，也不要直接去拆字符串，而要通过os.path.split()函数，
# 这样可以把一个路径拆分为两部分，后一部分总是最后级别的目录或文件名
os.path.split('/Users/michael/testdir/file.txt')

# os.path.splitext()可以直接让你得到文件扩展名，很多时候非常方便
os.path.splitext('/path/to/file.txt')

# 对文件重命名:
os.rename('test.txt', 'test.py')

# 删掉文件:
os.remove('test.py')

# 如何利用Python的特性来过滤文件。比如我们要列出当前目录下的所有目录，只需要一行代码
dir = [x for x in os.listdir('.') if os.path.isdir(x)]

# 要列出所有的.py文件，也只需一行代码：
file = [x for x in os.listdir('.') if os.path.isfile(x) and os.path.splitext(x)[1] == 'py']

