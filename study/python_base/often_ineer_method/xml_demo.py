# -*- coding: utf-8 -*-

# @Time : 2022/2/25 19:05

# @Author : WangJun

# @File : xml_demo.py

# @Software: PyCharm


# 在Python中使用SAX解析XML非常简洁，通常我们关心的事件是start_element，
# end_element和char_data，准备好这3个函数，然后就可以解析xml了

from xml.parsers.expat import ParserCreate

class DefaultSaxHandler(object):
    def start_element(self, name, attrs):
        print('sax:start_element: %s, attrs: %s' % (name, str(attrs)))

    def end_element(self, name):
        print('sax:end_element: %s' % name)

    def char_data(self, text):
        print('sax:char_data: %s' % text)

xml = r'''<?xml version="1.0"?>
<ol>
    <li><a href="/python">Python</a></li>
    <li><a href="/ruby">Ruby</a></li>
</ol>
'''
handler = DefaultSaxHandler()
parser = ParserCreate()
parser.StartElementHandler = handler.start_element
parser.EndElementHandler = handler.end_element
parser.CharacterDataHandler = handler.char_data
parser.Parse(xml)
