# -*- coding: utf-8 -*-

# @Time : 2022/2/25 17:47

# @Author : WangJun

# @File : struct_demo.py

# @Software: PyCharm

# Python提供了一个struct模块来解决bytes和其他二进制数据类型的转换

# struct的pack函数把任意数据类型变成bytes
import struct
struct.pack('>I', 10240099)
# pack的第一个参数是处理指令，'>I'的意思是：
#
# >表示字节顺序是big-endian，也就是网络序，I表示4字节无符号整数

# unpack把bytes变成相应的数据类型：
struct.unpack('>IH', b'\xf0\xf0\xf0\xf0\x80\x80')
# 根据>IH的说明，后面的bytes依次变为I：4字节无符号整数和H：2字节无符号整数