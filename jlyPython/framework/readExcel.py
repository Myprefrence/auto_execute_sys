#-*-coding:GBK -*-
import xlrd
import os
from xlwt import *

from xlrd import open_workbook

from xlutils.copy import copy
file_path = os.path.dirname(os.path.abspath('.')) + '/testFile/test.xls'
# file_path = os.path.abspath(os.curdir)+ '/testFile/test.xls'
class ReadExcel(object):

    def __init__(self, sheet_name):
        self.sheet_name = sheet_name

    @property
    def getSheet(self):
        # 获取索引
        xl = xlrd.open_workbook(file_path)
        sheet = xl.sheet_by_name(self.sheet_name)
        # print( xl.sheet_names() )   打印所有sheet名字
        # print (sheet.cell_value( 2, 3 ))   打印第3行第4列
        return sheet

    @property
    def getRows(self):
        # 获取行数
        row = self.getSheet.nrows
        return row

    @property
    def getCol(self):
        # 获取列数
        col = self.getSheet.ncols
        return col

    # 以下是分别获取每一列的数值

    @property
    def getId(self):
        TestId = []
        for i in range( 1, self.getRows):
            TestId.append( self.getSheet.cell_value(i, 0))
        # print(TestName)
        return TestId

    @property
    def getName(self):
        TestName = []
        for i in range(1, self.getRows):
            TestName.append(self.getSheet.cell_value(i, 1))
        # print(TestName)
        return TestName

    @property
    def getData(self):
        TestData = []
        for i in range(1, self.getRows):
            TestData.append(self.getSheet.cell_value(i, 2))
        return TestData

    @property
    def getUrl(self):
        TestUrl = []
        for i in range(1, self.getRows):
            TestUrl.append(self.getSheet.cell_value(i, 3))
        return TestUrl

    @property
    def getMethod(self):
        TestMethod = []
        for i in range(1, self.getRows):
            TestMethod.append(self.getSheet.cell_value(i, 4))
        return TestMethod

    @property
    def getStatusCode(self):
        TestUid = []
        for i in range(1, self.getRows):
            TestUid.append(self.getSheet.cell_value(i, 5))
        return TestUid

    @property
    def getCode(self):
        TestCode = []
        for i in range(1, self.getRows):
            TestCode.append(self.getSheet.cell_value(i, 6))
        return TestCode

    @property
    def getStatus(self):
        getStatus = []
        for i in range(1, self.getRows):
            getStatus.append(self.getSheet.cell_value(i, 7))
        return getStatus

    @property
    def getEncryption(self):
        getEncryption = []
        for i in range(1, self.getRows):
            getEncryption.append(self.getSheet.cell_value(i, 8))
        return getEncryption



    def result_write(self, result):

        for i in range(1, self.getRows):
            book = open_workbook(file_path)
            # sheet = book.add_sheet(self.sheet_name)
            wb = copy(book)
            ws = wb.get_sheet(self.sheet_name)
            ws.write(i, 6, result)
            wb.save(file_path)
            # book.save(file_path)


