import time

import pymysql,json
from pymysql.constants import CLIENT
# 连接数据库
con = pymysql.connect(host="172.16.11.92", user="root", \
                      password="HRdXK3TelK6bgGyg",\
                      # db="fresho2o",\
                      charset="utf8",\
                      cursorclass=pymysql.cursors.DictCursor,\
                      client_flag=CLIENT.MULTI_STATEMENTS)

class variableSql(object):
    def __init__(self,xn,env):
        self.xn = xn
        self.env = env

    def varCode(self,code):
        # 获取变量编码
        cur = con.cursor()
        cur.execute('SELECT DISTINCT(invoke_interface_code) FROM %s_fes.t_var_base_info WHERE var_code in ("%s");' % (
        self.env,code))
        da = cur.fetchall()
        co = da[0]["invoke_interface_code"]
        print("变量接口编码:",co)
        return co

    def updateHuiSu(self,applyno, applyid, orderno,HuisuTime):
        # 回溯订单
        cur = con.cursor()
        # 执行查询用户名和密码的sql语句
        cur.execute('select * from %s_res.t_case_apply_log where apply_no = "%s";' % (self.env, applyno))
        # 获取记录
        data = cur.fetchall()
        applyDate = data[0]["apply_datetime"]
        datee = json.dumps(applyDate, cls=DateEncoder)
        if datee != HuisuTime:
            cur.execute(
                'update %s_res.t_case_apply_log set apply_datetime = "%s" where apply_no = "%s";' % (
                self.env, HuisuTime,applyno))
            cur.execute(
                'update %s_res.t_case_apply_log set create_datetime = "%s" where apply_no = "%s";' % (
                self.env, HuisuTime,applyno))
            con.commit()
            print('回溯订单申请时间\创建时间更新成功')
        else:
            print("回溯订单申请时间造数失败，请手动执行sql")
        # 回溯订单内部变量
        cur.execute('DELETE FROM %s_fes.t_request_info  WHERE case_id = "%s";' % (self.env, applyid))
        con.commit()
        print('回溯订单内部变量清除更新成功')

    def cbsUpdate(self,orderno,loanDate):
        # cbs订单管理创建时间更新
        cur = con.cursor()
        cur.execute('select * from %s_%s_cbs.t_loan_order where asset_loan_order_no="%s";' % (self.xn, self.env, orderno))
        up = cur.fetchall()
        # print(up[0][21])
        createDate = up[0]["create_datetime"]
        datee1 = json.dumps(createDate, cls=DateEncoder)
        if datee1 != loanDate:
            cur.execute(
                'update %s_%s_cbs.t_loan_order set create_datetime = "%s" where asset_loan_order_no = "%s";' % (
                self.xn, self.env,loanDate, orderno))
            con.commit()
            print('cbs订单管理创建时间更新成功')
        else:
            print("cbs订单管理创建时间造数失败，请手动执行sql")

    def updateCreate(self,num, orderno,loanDate):
        # 修改被造数据--实还金额=应还金额
        cur = con.cursor()
        cur.execute(
            'update %s_%s_cbs.t_repay_plan set rpy_total_amt = "%s" where asset_loan_order_no = "%s" and type = "CBS" order by schedule_date ;' % (
            self.xn,self.env,num, orderno))
        con.commit()
        print("修改实还金额=应还金额成功")

    def updateTime1(self,orderno):
        #应还时间>实还时间
        cur = con.cursor()
        cur.execute(
            'update %s_%s_cbs.t_repay_plan set last_rpy_datetime = date_sub(schedule_date,interval 2 day) where asset_loan_order_no = "%s" and type = "CBS" order by schedule_date ;' % (
            self.xn, self.env, orderno))
        con.commit()
        print("应还时间>实还时间造数成功")

    def updateTime2(self,orderno):
        #应还时间<实还时间
        cur = con.cursor()
        cur.execute(
            'update %s_%s_cbs.t_repay_plan set last_rpy_datetime = date_add(schedule_date,interval 2 day) where asset_loan_order_no = "%s" and type = "CBS" order by schedule_date ;' % (
            self.xn, self.env, orderno))
        con.commit()
        print("应还时间<实还时间造数成功")
    def updateTime3(self,orderno):
        #应还时间=实还时间
        cur = con.cursor()
        cur.execute(
            'update %s_%s_cbs.t_repay_plan set last_rpy_datetime = schedule_date where asset_loan_order_no = "%s" and type = "CBS" order by schedule_date ;' % (
            self.xn, self.env, orderno))
        con.commit()
        print("应还时间=实还时间造数成功")
    def result(self,applyid,interface_code,code):
        #查询回溯返回的结果
        cur = con.cursor()
        aa = 1
        while True:
            cur.execute('SELECT resp_result FROM %s_fes.t_invoke_result_record  WHERE case_id ="%s" \
                and interface_code = "%s" ORDER BY update_datetime DESC limit 1;' % (self.env, applyid, interface_code))
            resut = cur.fetchall()
            a = resut[0]["resp_result"]
            if a is not None:
                b = json.loads(a)
                print("查询回溯结果成功！%s ：" % code, b[code])
                print(a)
                break
            else:
                print("等待回溯结果返回...")
                aa = aa + 1
                time.sleep(1.5)
                if aa>=5:
                    print('等待回溯结果超时，请手动查询')
                    break



def varCode(env,code):
    #获取变量编码
    cur = con.cursor()
    cur.execute('SELECT DISTINCT(invoke_interface_code) FROM %s_fes.t_var_base_info WHERE var_code in ("%s");'%(env,code))
    da = cur.fetchall()
    print("变量接口编码为：",da)

if __name__ == '__main__':
    # variableSql("xna","test1").varCode("userid_grt_ever_overdue_cnt_tot")
    variableSql("xna", "test1").result("XNAA032206170015730006","userLoanDetailVar","userid_self_prod_early_settle_cnt_tot")