from HuiSu import *

if __name__ == '__main__':
    loanDate = "2021-07-05 00:00:00"
    project = "test222"
    custName = "海飞三"
    xn = "xna"
    env = "test1"
    """客户身份证id"""
    id = "110101201107743313"
    mobile = "15846457801"
    loan_term = 4
    loanAmt = 400
    num = loanAmt / loan_term + 10
    less_num = loanAmt / loan_term
    a = send(xn, env).main(1, project, loanDate, id, mobile, custName, loan_term, loanAmt)
    time.sleep(2)
    if a[0] is None:
        orderno = a[1]
        exit(1)
    else:
        applyno = a[0]["apply_no"]
        applyid = a[0]["id"]
        orderno = a[1]
    # cbs订单管理创建时间更新
    send(xn, env).cbsUpdate(orderno, loanDate)
    # 变量接口编码查询
    code = 'userid_grt_ever_overdue_cnt_tot'
    interface_code = variableSql(xn, env).varCode(code)
#################################################################################
    # # 修改回溯案件
    # HuisuTime = "2022-01-01 00:00:00"
    # send(xn, env).updateHuiSu(applyno, applyid, orderno, HuisuTime)
    # # 执行回溯案件
    # time.sleep(2)
    # cookie = testDemo(env).login()
    # testDemo(env).Huisu(applyid, interface_code, cookie)
    # # 查询回溯后变量的结果
    # variableSql(xn, env).result(applyid,interface_code,code)
#################################################################################
    # 修改被造数据---应还金额=实还金额,应还时间=实还时间
    # send(xn,env).updateCreate(num,orderno,loanDate)
    # send(xn, env).updateTime3(orderno)
    # # 修改被造数据---应还金额=实还金额,应还时间<实还时间
    # send(xn,env).updateCreate(num,orderno,loanDate)
    # send(xn,env).updateTime2(orderno)
    # # 修改被造数据---应还金额=实还金额,应还时间>实还时间(提前结清,默认提前结清2天)
    # send(xn,env).updateCreate(num, orderno, loanDate)
    # send(xn,env).updateTime1(orderno)
    # # 修改被造数据---应还金额>实还金额,应还时间=实还时间
    # send(xn,env).updateCreate(less_num,orderno,loanDate)
    # send(xn, env).updateTime3(orderno)
    # # 修改被造数据---应还金额>实还金额,应还时间<实还时间(逾期，默认逾期3天)
    send(xn,env).updateCreate(less_num,orderno,loanDate)
    send(xn, env).updateTime2(orderno)
    # # 修改被造数据---应还金额>实还金额，应还时间>实还时间(提前结清,默认提前结清2天)
    # send(xn,env).updateCreate(less_num,orderno,loanDate)
    # send(xn, env).updateTime1(orderno)

