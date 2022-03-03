# auto_execute_sys

[目的]
提升测试效率、测试工具集成

[集成者]
汪军 黄海峰

[目录映射关系]  
business    存放与业务相关的接口代码
database    存放与数据库操作相关的代码
request     存放与请求方法相关的代码
params      存放测试数据
common      存放公共方法
config      存放配置文件
logs        存放日志文件
file        存放其他文件
study       存放学习代码

[使用]
1. 更新项目所需要的模块依赖
python -m pip install -r requirements.txt

2. 代码对应的需求
channl_od.py 造通道数据
field_map.py 通用字段映射需求代码
sendOrder.py 批量造订单数据
sendOrder_1.py 自定义造订单数据
repay_record.py 根据订单号生成还款记录和还款计划
offlineOrder.py 造离线跑批数据
suspend.py 造卡件数据
trends_control.py 造动态控件数据 (Redis)
