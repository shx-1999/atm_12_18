'''
用户功能接口
'''
import os,time
from db import models
from conf import setting
from lib import common

# 实例出日志对象
user_logger = common.loggin_record("login")


def login_api(name,passwd):
    '''
    用户登入接口
    :param name: 用户名
    :param passwd: 用户密码
    :return:
    '''
    user_path = os.path.join(setting.DB_PATH,f"{name}.json")
    if os.path.isfile(user_path):
        user_dic = models.check(name)
        if user_dic["lock"] is True:
            return None, "该用户已锁定,请联系管理员"
        elif passwd == user_dic["passwd"]:
            user_logger.info(f"用户:{name}登入了")
            user_dic["logfile"].append(f"{time.strftime('%Y-%m-%d %X',time.localtime(time.time()))} 用户:{name}登入了")
            return True, "登入成功"
        else:
            return False, "密码错误"
    else:
        return None,"用户不存在"





def register_api(name,passwd):
    '''
    用户注册接口
    :param name:用户名
    :param passwd:用户密码
    :return:
    '''
    user_dic = {
            "name":name,
            "passwd":passwd,
            "balan":10000,
            "shops":{},
            "logfile":[],
            "lock":False
        }
    user_dic["logfile"].append(f"{time.strftime('%Y-%m-%d %X',time.localtime(time.time()))} 当前用户:{name}注册成功")
    models.save(user_dic)
    user_logger.info(f"用户:{name}注册成功")
    return "恭喜注册注册成功"




def user_active(name):
    '''
    查看个人操作日志接口
    :param name:
    :return:
    '''
    user_dic = models.check(name)
    user_logger.info(f"用户:{name}查看了个人流水")

    return user_dic["logfile"]


