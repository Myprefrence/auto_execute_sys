# -*- coding: utf-8 -*-

# @Time : 2022/2/25 14:39

# @Author : WangJun

# @File : file_read_write.py

# @Software: PyCharm


f = open('test.txt', 'r', encoding="utf-8")
print(f.read())
# 最后一步是调用close()方法关闭文件。文件使用完毕后必须关闭，因为文件对象会占用操作系统的资源，
# 并且操作系统同一时间能打开的文件数量也是有限的
f.close()

with open('test.txt', 'r') as f:
    print(f.read())


# 如果文件很小，read()一次性读取最方便；如果不能确定文件大小，反复调用read(size)比较保险；
# 如果是配置文件，调用readlines()最方便
# for line in f.readlines():
#     print(line.strip()) # 把末尾的'\n'删掉


# 二进制文件
# 前面讲的默认都是读取文本文件，并且是UTF-8编码的文本文件。要读取二进制文件，
# 比如图片、视频等等，用'rb'模式打开文件即可：

fg = open('202201191409.jpg', 'rb')
print(fg.read())

# 字符编码
# 要读取非UTF-8编码的文本文件，需要给open()函数传入encoding参数，例如，读取GBK编码的文件
# 遇到有些编码不规范的文件，你可能会遇到UnicodeDecodeError，因为在文本文件中可能夹杂了一些非法编码的字符。
# 遇到这种情况，open()函数还接收一个errors参数，表示如果遇到编码错误后如何处理。最简单的方式是直接忽略：
fz = open('test.txt', 'r', encoding='utf-8', errors='ignore')
fz.read()
fz.close()

# 写文件
# 写文件和读文件是一样的，唯一区别是调用open()函数时，传入标识符'w'或者'wb'表示写文本文件或写二进制文件：
fw = open('/Users/michael/test.txt', 'w')
fw.write("hello")
fw.close()