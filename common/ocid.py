import csv
import os
import random

"""
    1. 前1-2位数字代表所省份代码
    2. 第3-4位数字代表所城市代码
    3. 第5-6位数字代表所区县代码
    4. 第7-14位数字代表的是: 第7-10位为出生年份, 第11-12位代表出生月份, 第13-14位代表出生日期
    5. 第15-17位是顺序码, 同一地址码所标识的区域范围内, 对同年-月-日出生的人员编定的顺序号, 其中第十七位奇数分给男性, 偶数分给女性
    6. 第18位数字为校检码: 校检码0-9数字, 10用X表示, 这是根据前面十七位数字码, 按照ISO 7064:1983.MOD 11-2校验码计算出来的检验码

    ISO 7064:1983.MOD 11-2校验码的例子:
        十七位数    1     2     3     4     5     6     7     8     9     0     1     2     3     4     5     6     7
        加权因子    7     9     10    5     8     4     2     1     6     3     7     9     10    5     8     4     2
        计算十七位数字各位数字与对应的加权因子的乘积的和S:
            1×7＋2×9＋3×10＋4×5＋5×8＋6×4＋7×2＋8×1＋9×6＋0×3＋1×7＋2×9＋3×10＋4×5＋5×8＋6×4＋7×2 = 368
        计算S/11的余数T: 
            368 % 11＝5
        余数0－10对应校验码为[1, 0, X , 9, 8, 7, 6, 5, 4, 3, 2], 算法如下:
        计算(12-T)/11的余数R, 如果R＝10, 校验码为字母X; 如果R≠10, 校验码为数字R: （12-5）mod 11＝7
        该17位数字的校验码就是7, 聚合在一为123456789012345677
"""


class CreateIdCardNumber:
    """
    @desc 生成身份证号码

    :param numbers 生成的身份证号数量
    """

    def __init__(self, numbers=1):
        self.numbers = numbers
        self.id_card_numbers = []

    @staticmethod
    def get_administrative_division_code():
        """获取行政区划编码"""
        # 拼接文件的地址
        filename = os.path.dirname(
            os.path.realpath(__file__)) + '/行政区划代码.csv'
        # 读取行政区划编码的csv文件
        with open(filename, 'r', encoding='UTF-8') as f:
            reader = csv.reader(f)
            # 存放行政区划编码
            administrative_division_codes = []
            # 逐一遍历，不存在就跳过，存在就加入
            for row in reader:
                try:
                    number = row[0]
                except ValueError:
                    print(f"Missing data {row[1]}")
                else:
                    administrative_division_codes.append(number)
        # 将行政区划编码列表返回去
        return administrative_division_codes[1:]

    @staticmethod
    def year_month_day():
        # 用来存放生成的年月日
        year_month_day = []
        # 生成500个日期
        number = 500
        while number != 0:
            # 随机生成年月
            year = str(random.randint(1990, 2000))
            month = str(random.randint(1, 12)).zfill(2)
            # 根据月份确定天的随机数
            if month in ['01', '03', '05', '07', '08', '10', '12']:
                day = str(random.randint(1, 31)).zfill(2)
            elif month in ['04', '06', '09', '11']:
                day = str(random.randint(1, 30)).zfill(2)
            else:
                day = str(random.randint(1, 29)).zfill(2)
            # 临时存放生成的年月日，好用于后面的判断
            result = year + month + day
            if result not in year_month_day:
                year_month_day.append(result)
                number -= 1
        # 将年月日列表返回
        return year_month_day

    @staticmethod
    def sequence_code():
        # 用来存放生成的顺序码
        sequence_code = []
        # 生成500个顺序码
        number = 500
        while number != 0:
            # 直接对1000进行取随机值
            # 临时存放随机值，好用于后面的判断
            result = str(random.randint(0, 1000)).zfill(3)
            if result not in sequence_code:
                sequence_code.append(result)
                number -= 1
        # 将生成的顺序码返回
        return sequence_code

    def check_code(self):
        # 通过调用前面的函数生成17个字符的字符串
        digits = random.choices(self.get_administrative_division_code())[0] + \
                 random.choices(
                     self.year_month_day())[0] + \
                 random.choices(self.sequence_code())[0]
        # 根据ISO 7064:1983.MOD 11-2校验码算法
        # 要用不足补0，应为可能为空
        try:
            temporary_check_code = (12 - (
                    int(digits[0:1].zfill(1)) * 7 + int(
                digits[1:2].zfill(1)) * 9 + int(
                digits[2:3].zfill(1)) * 10 + int(
                digits[3:4].zfill(1)) * 5 + int(
                digits[4:5].zfill(1)) * 8 + int(
                digits[5:6].zfill(1)) * 4 + int(
                digits[6:7].zfill(1)) * 2 + int(
                digits[7:8].zfill(1)) * 1 + int(
                digits[8:9].zfill(1)) * 6 + int(
                digits[9:10].zfill(1)) * 3 + int(
                digits[10:11].zfill(1)) * 7 + int(
                digits[11:12].zfill(1)) * 9 + int(
                digits[12:13].zfill(1)) * 10 + int(
                digits[13:14].zfill(1)) * 5 + int(
                digits[14:15].zfill(1)) * 8 + int(
                digits[15:16].zfill(1)) * 4 + int(
                digits[16:17].zfill(1)) * 2) % 11) % 11
        except Exception as f:
            # 出错了就将错误信息打印出来
            print(f)
        else:
            # 如果校验码是10就转换为x,其他的就去其数值
            check_code = str(
                temporary_check_code) if temporary_check_code != 10 else 'x'
            # 将生成的以为校验码返回
            return check_code

    def create_id_card_number(self):
        """生成身份证号码"""
        # 在给定的数内循环
        while self.numbers != 0:
            # 临时存放生成的身份证号码，好用于后面的判断
            result = random.choices(self.get_administrative_division_code())[
                         0] + random.choices(self.year_month_day())[0] + \
                     random.choices(
                         self.sequence_code())[0] + self.check_code()
            # 判断，存在就跳过，否者就加入
            if result not in self.id_card_numbers:
                self.id_card_numbers.append(result)
                self.numbers -= 1
        # 将生成的身份证号码返回
        return self.id_card_numbers


if __name__ == '__main__':
    print((CreateIdCardNumber(1).create_id_card_number()))
