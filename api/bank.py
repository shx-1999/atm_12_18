import os,time
from db import models
from conf import setting
from lib import common

# 实例出日志对象
bank_loggin = common.loggin_record('transaction')


def balance_api(name):
    '''
    查询余额接口
    :param name:
    :return:
    '''
    user_dic = models.check(name)
    bank_loggin.info(f"用户:{name}查看了余额")
    user_dic["logfile"].append(f"{time.strftime('%Y-%m-%d %X',time.localtime(time.time()))} 我查看了余额")
    models.save(user_dic)
    return user_dic["balan"]



def transfer_api(from_name,to_name,money):
    '''
    转账接口
    :param fron_name:转账用户
    :param to_name:被转账用户
    :return:
    '''
    to_user_path = os.path.join(setting.DB_PATH,f"{to_name}.json")
    if os.path.isfile(to_user_path):
        from_dic = models.check(from_name)
        to_dic = models.check(to_name)
        if from_dic["balan"] >= money*1.05:
            from_dic["balan"] -= money*1.05
            to_dic["balan"] += money
            from_dic["logfile"].append(f"{time.strftime('%Y-%m-%d %X',time.localtime(time.time()))} 我向用户:{to_name}转账了{money}元,扣除了手续费{money * 0.05:.2f}元")
            models.save(from_dic)
            to_dic["logfile"].append(f"{time.strftime('%Y-%m-%d %X',time.localtime(time.time()))} 用户:{from_name}向我转账了{money}元")
            models.save(to_dic)
            bank_loggin.info(f"用户:{from_name}向用户:{to_name}转账了{money}元,扣除了手续费{money * 0.05:.2f}元")
            return True,"转账成功"
        else:
            return False,"余额不足"
    else:
        return False,"对方用户账号不存在"


def withdraw_api(name,money):
    '''
    取款接口
    :param name:用户名
    :param money:金额
    :return:
    '''
    user_dic = models.check(name)
    if user_dic["balan"] >= money*1.05:
        user_dic["balan"] -= money*1.05
        user_dic["logfile"].append(f"{time.strftime('%Y-%m-%d %X',time.localtime(time.time()))} 我从账户中取走了:{money}元,扣除手续费:{money*0.05:.2f}元")
        models.save(user_dic)
        bank_loggin.info(f"用户:{name}从账户中取走了:{money}元,扣除手续费:{money*0.05:.2f}元")
        return True,"取款成功"
    else:
        return False,"余额不足"


def repayment_api(name,money):
    '''
    还款接口
    :param name:
    :param money:
    :return:
    '''
    user_dic = models.check(name)
    user_dic["balan"] += money
    user_dic["logfile"].append(f"{time.strftime('%Y-%m-%d %X',time.localtime(time.time()))} 我进行了还款操作,金额:{money}元")
    models.save(user_dic)
    bank_loggin.info(f"用户:{name}进行了还款操作,还款金额:{money}元")
    return "还款成功"

