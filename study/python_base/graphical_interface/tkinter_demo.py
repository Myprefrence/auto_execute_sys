# -*- coding: utf-8 -*-

# @Time : 2022/3/2 10:20

# @Author : WangJun

# @File : tkinter_demo.py

# @Software: PyCharm

from tkinter import *
import tkinter.messagebox as messagebox

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    # 在GUI中，每个Button、Label、输入框等，都是一个Widget。Frame则是可以容纳其他Widget的Widget，
    # 所有的Widget组合起来就是一棵树。
    #
    # pack()方法把Widget加入到父容器中，并实现布局。pack()是最简单的布局，grid()可以实现更复杂的布局。
    #
    # 在createWidgets()
    # 方法中，我们创建一个Label和一个Button，当Button被点击时，触发self.quit()使程序退出。
    def createWidgets(self):
        # self.helloLabel = Label(self, text='Hello, world!')
        # self.helloLabel.pack()
        # self.quitButton = Button(self, text='Quit', command=self.quit)
        # self.quitButton.pack()
        self.nameInput = Entry(self)
        self.nameInput.pack()
        self.alertButton = Button(self, text='Hello', command=self.hello)
        self.alertButton.pack()

    def hello(self):
        name = self.nameInput.get() or 'world'
        messagebox.showinfo('Message', 'Hello, %s' % name)

app = Application()
# 设置窗口标题:
app.master.title('Hello World')
# 主消息循环:
app.mainloop()

# 当用户点击按钮时，触发hello()，通过self.nameInput.get()获得用户输入的文本后，使用tkMessageBox.showinfo()
# 可以弹出消息对话框。

