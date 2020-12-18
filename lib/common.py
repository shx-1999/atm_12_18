'''
公共功能
'''
import logging.config,time
from conf import setting
from core import src
from db import models


# 登入认证装饰器
def login_auth(func):
    def wrapper(*args,**kwargs):
        if not src.login_user["name"] is None:
            return func(*args,**kwargs)
        else:
            print("请登入后使用该功能")
            src.login()
    return wrapper


# 日志记录功能
def loggin_record(name):
    logging.config.dictConfig(setting.LOGGING_DIC)  # 使用这个日志字典
    logger = logging.getLogger(name)                # 实例出日志对象
    return logger

# 实例一个 "login" 对象
user_loggin = loggin_record('login')


# 用户锁定功能
def locker(name):
    user_dic = models.check(name)
    user_dic["lock"] = True
    models.save(user_dic)
    user_loggin.info(f'用户{name}已被锁定')
    user_dic["logfile"].append(f"{time.strftime('%Y-%m-%d %X',time.localtime(time.time()))} 当前用户{name}已被锁定")
    return

# 解锁用户功能
def unlock(name):
    user_dic = models.check(name)
    user_dic["lock"] = False
    user_loggin.info(f'用户{name}已经解除解锁')
    user_dic["logfile"].append(f"{time.strftime('%Y-%m-%d %X',time.localtime(time.time()))} 当前用户{name}已经解除解锁")
    models.save(user_dic)
    return
