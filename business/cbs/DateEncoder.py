# datetime.datetime(2022, 1, 1, 00, 00, 00)
# 以上时间格式转换成正常格式
import datetime
import json
class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return json.JSONEncoder.default(self, obj)


dic = datetime.datetime(2022, 1, 1, 00, 00, 00)
datee = json.dumps(dic, cls=DateEncoder)
print(datee)
