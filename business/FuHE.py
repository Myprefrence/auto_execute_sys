from business.platform1 import JlyPlatform

jly = JlyPlatform(environment='test1', virtual='xna')
#复核策略
jly.do_audit_strategy(strategy_code='C222')
#复核项目
# jly.audit_project('A002')


