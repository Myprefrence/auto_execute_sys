import os
from json.decoder import JSONDecodeError

import jsonpath
import xlrd
import datetime
from xlrd import xldate_as_tuple
import xlwt
from io import BytesIO
import json
import time



class fieldMap:

    def __init__(self, sheetname):
        # 文件路径
        self.root_dir = os.path.dirname(os.path.abspath('..')) + r'\config\maping.xls'
        # 定义一个属性接收工作表名称
        self.sheetname = sheetname
        # 使用xlrd模块打开excel表读取数据
        self.data = xlrd.open_workbook(self.root_dir)
        # 根据工作表的名称获取工作表中的内容（方式①）
        self.table = self.data.sheet_by_name(self.sheetname)
        # 根据工作表的索引获取工作表的内容（方式②）
        # self.table = self.data.sheet_by_name(0)
        # 获取第一行所有内容,如果括号中1就是第二行，这点跟列表索引类似
        self.keys = self.table.row_values(0)
        # 获取工作表的有效行数
        self.rowNum = self.table.nrows
        # 获取工作表的有效列数
        self.colNum = self.table.ncols


    def red_excel(self):
        # 定义一个空列表
        datas = []
        for i in range(1, self.rowNum):
            # 定义一个空字典
            sheet_data = {}
            for j in range(self.colNum):
                # 获取单元格数据类型
                c_type = self.table.cell(i, j).ctype
                # 获取单元格数据
                c_cell = self.table.cell_value(i, j)
                if c_type == 2 and c_cell % 1 == 0:  # 如果是整形
                    c_cell = int(c_cell)
                elif c_type == 3:
                    # 转成datetime对象
                    date = datetime.datetime(*xldate_as_tuple(c_cell,0))
                    c_cell = date.strftime('%Y/%d/%m %H:%M:%S')
                elif c_type == 4:
                    c_cell = True if c_cell == 1 else False
                sheet_data[self.keys[j]] = c_cell
                # 循环每一个有效的单元格，将字段与值对应存储到字典中
                # 字典的key就是excel表中每列第一行的字段
                # sheet_data[self.keys[j]] = self.table.row_values(i)[j]
            # 再将字典追加到列表中
            datas.append(sheet_data)
        # 返回从excel中获取到的数据：以列表存字典的形式返回
        return datas


    def write_excel(self,data):
        # print(data)
        # 操作内存的
        stream = BytesIO()
        # 写入excel格式数据
        workbook = xlwt.Workbook(encoding='utf-8')
        file = workbook.add_sheet(self.sheetname)
        style = xlwt.XFStyle()
        style_1 = xlwt.XFStyle()
        # 设置字体位置
        al = xlwt.Alignment()
        al.horz = 0x02  # 设置水平居中
        al.vert = 0x01  # 设置垂直居中
        style.alignment = al

        # 设置背景颜色
        pattern = xlwt.Pattern()
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = xlwt.Style.colour_map['yellow']
        style.pattern = pattern
        # 单元格边框设置
        borders = xlwt.Borders()
        borders.left = 1
        borders.right = 1
        borders.top = 1
        borders.bottom = 1
        style.borders = borders
        style_1.borders = borders
        # 标题
        title = ["序号", "credit_value", "cbs_value", "rms_value",  "res_value", "result"]
        for col_index in range(0, len(title)):
            # 设置行高
            file.row(col_index).height_mismatch = True
            file.row(col_index).height = 20*40  #20为基准数，40意为40磅
            file.write(0, col_index, title[col_index], style)
        # 主体数据
        for row_index in range(1, len(data) + 1):
            # print("row_index:%s" % (row_index, ))
            temp = data[row_index - 1]

            file.write(row_index, 0, row_index, style_1)
            for col_index in range(1, len(temp) + 1):
                # 设置表格宽度
                file.col(col_index).width = 256 * 35
                value = temp[col_index - 1]
                # datime数据转下格式
                if isinstance(value, datetime.datetime):
                    value = value.strftime('%Y-%m-%d %H:%M:%S')
                file.write(row_index, col_index, value, style_1)
        # 文件内容保存在内存中
        workbook.save(stream)
        # 直接从内存中返回数据
        return stream.getvalue()

    def getNonRepeatList(self,data):
        new_data = []
        for i in range(len(data)):
            if data[i] not in new_data:
                new_data.append(data[i])
        return new_data

    def get_valuelist_by_key(self, json_data, find_key):
        """根据find_key查询json_data中所有的value 返回所有满足条件的列表--深度遍历

        :param json_data: 匹配的json字符串，json_data必须为dict或者list
        :param find_key: key名
        :return: 多个匹配值
        """
        values_list = []

        def get_value_list(json, key):
            nonlocal values_list
            if isinstance(json, dict):
                for item, values in json.items():
                    if str(item) == str(key):
                        values_list.append(str(json.get(item)))
                    if isinstance(values, dict):
                        get_value_list(values, key=key)
                    if isinstance(values, list):
                        get_value_list(values, key=key)
                    else:
                        pass
            elif isinstance(json, list):
                for data in json:
                    if isinstance(data, dict):
                        get_value_list(data, key)
            else:
                return []
            return values_list

        return get_value_list(json=json_data, key=find_key)

    def turn_json_to_dict(self,target_data: str or dict):
        if type(target_data) == dict:
            for key in target_data:
                value = target_data[key]
                try:
                    dict_data = json.loads(value)
                except (json.decoder.JSONDecodeError, TypeError):
                    pass
                else:
                    if type(dict_data) == dict:
                        target_data[key] = dict_data
                        self.turn_json_to_dict(dict_data)

        return target_data

    def get_value_by_all_keys(self, target_dict: dict, target_key: str, result_list=None):
        if result_list is None:
            result_list = []
        try:
            result_list.append(target_dict[target_key])
        except KeyError:
            for param in target_dict:
                dict_data = target_dict[param]
                try:
                    json_data = json.loads(dict_data)

                except (json.decoder.JSONDecodeError, TypeError):
                    if type(dict_data) == dict:
                        self.get_value_by_all_keys(dict_data, target_key, result_list=result_list)
                    if type(dict_data) == list:
                        for list_data in dict_data:
                            if type(list_data) == dict:
                                self.get_value_by_all_keys(list_data, target_key, result_list=result_list)
                else:
                    if type(json_data) == dict:
                       self.get_value_by_all_keys(json_data, target_key, result_list=result_list)

            return result_list

    def jsonPath_get_value(self,json_data, find_key):

        if json_data is not None and find_key is not None:
            try:
                value = jsonpath.jsonpath(json_data, find_key)
                if value == False:
                    return []
                else:
                    return value

            except Exception as e:
                print("解析异常，message: %s" % (e,))

        else:
            print("json_data or find_key为空")


    def handle_credit_map(self):

        get_data = self.red_excel()
        # print(get_data)

        credit = []


        for credit_data in get_data:
            # print(maps_data)
            credit_key = credit_data["credit字段"]
            credit_file = os.path.dirname(os.path.abspath('..')) + r'\config\credit.json'
            with open(credit_file, 'r', encoding='utf-8') as f:
                json_data = json.load(f)

                cbs_d = self.get_valuelist_by_key(json_data, credit_key)
                credit.append(cbs_d)
        f.close()

        return credit

    def handle_cbs_map(self):

        get_data = self.red_excel()
        # print(get_data)

        cbs = []


        for cbas_data in get_data:
            # print(maps_data)
            cbs_key = cbas_data["cbs字段"]
            cbs_file = os.path.dirname(os.path.abspath('..')) + r'\config\cbs.json'
            with open(cbs_file, 'r', encoding='utf-8') as f:
                json_data = json.load(f)

                cbs_d = self.get_valuelist_by_key(json_data, cbs_key)
                cbs.append(cbs_d)
        f.close()

        return cbs

    def handle_rms_map(self):
        get_data = self.red_excel()
        rms = []
        new_dict = {}
        for rmsss_data in get_data:
            # print(maps_data)
            rms_key = rmsss_data["rms字段"]
            rms_file = os.path.dirname(os.path.abspath('..')) + r'\config\rms.json'

            with open(rms_file, 'r', encoding='utf-8') as f:
                json_param = f.read()
                json_data = json.loads(json_param)
                json_data = self.turn_json_to_dict(json_data)
                rms_d = self.jsonPath_get_value(json_data, rms_key)
                rms.append(rms_d)
        f.close()

        return rms

    def handle_res_map(self):

        get_data = self.red_excel()
        res = []

        for resss_data in get_data:
            # print(maps_data)
            res_key = resss_data["res字段"]
            cbs_file = os.path.dirname(os.path.abspath('..')) + r'\config\res.json'
            with open(cbs_file, 'r', encoding='utf-8') as f:
                json_data = json.load(f)

                res_d = self.get_valuelist_by_key(json_data, res_key)
                res.append(res_d)
        f.close()

        return res

    def conn_handle(self,):
        credit_array = []
        ces = self.handle_credit_map()
        for c_array in ces:
            array_ces = self.getNonRepeatList(c_array)
            credit_array.append(array_ces)

        cbs_array = []
        cbs = self.handle_cbs_map()
        for c_array in cbs:
            array_cbs = self.getNonRepeatList(c_array)
            cbs_array.append(array_cbs)

        # # print("cbs的json串：%s" % (cbs, ))
        rms_array = []
        rms = self.handle_rms_map()

        for m_array in rms:
            array_rms = self.getNonRepeatList(m_array)

            rms_array.append(array_rms)

        # print("rms的json串：%s" % (rms, ))
        res_array = []
        res = self.handle_res_map()
        for r_array in res:
            array_res = self.getNonRepeatList(r_array)
            res_array.append(array_res)
        # print("res的json串：%s" % (res,))

        list_f_new = []  # 最终结果
        if len(credit_array) == 0 and len(cbs_array) == 0 and len(rms_array) == 0 and len(res_array) == 0:
            print("值缺失")
        else:
            time.sleep(1.5)

        for length in range(len(cbs_array)):

            list_s_new = []

            for list_i in (credit_array, cbs_array, rms_array, res_array):
                if len(list_i[length]) == 0:
                    list_s_new.append('')

                for a in list_i[length]:

                    list_s_new.append(a)

            list_f_new.append(list_s_new)

        i = 0
        print(list_f_new)
        for array in list_f_new:
            number = set(array)

            if len(number) == 1:
                list_f_new[i].append('True')
            else:
                list_f_new[i].append('False')

            i += 1

        value = self.write_excel(list_f_new)
        file = os.path.dirname(os.path.abspath('..')) + r'\config\map.xls'

        if os.path.exists(file):
            os.remove(file)

        f = open(file=file, mode="wb")
        f.write(value)
        f.close()


if __name__ =='__main__':

    sheetname = "厚沃"
    get_data = fieldMap(sheetname)
    get_data.conn_handle()















