'''
程序核心逻辑+用户视图程序
功能 :
    注册, 登入, 查看余额, 取款, 还款, 转账, 查看个人操作日志(包括流水,日志会打印到终端,也会保存到日志文件), 购物, 查看购物车商品
    管理员功能:
        锁定用户, 解锁用户, 添加用户, 删除用户, 修改用户额度, 查看用户金额流动日志, 查看用户操作日志, 查看管理员操作日志
'''
from api import user,shop,bank,root
from lib import common
from db import models
from conf import setting


# 字体颜色
rr = '\033[0m'
ll = '\033[1;30;46m'
lll = '\033[1;31m'
llll = '\033[1;36m'
lllll = '\033[1;34m'


# 判断用户是否登入
login_user = {"name":None}

# 退出登入
def logout():
    if login_user["name"]:
        login_user["name"] = None
        print("\n退出成功")
    else:
        print("未登入,无需退出")


# 注册功能
def register():
    if not login_user["name"] is None:
        print("您当前正在登入,请退出到初始界面注册用户")
        return
    print(f"\n{ll}正在注册新账户...{rr}")
    print(f"注册须知：{lll}用户名必须大于3位，密码只能由数字或字母组成{rr}")
    while 1:
        name = input("请输入账号名(q退出)>>").strip()
        if name.lower() == "q": return
        if models.check(name):
            print("用户名已存在,请重新选择用户名")
            continue
        if len(name) <= 3:
            print(f"{ll}用户名不能小于3位{rr}")
            continue
        passwd = input("请输入密码>>").strip()
        if len(passwd) == 0 or not passwd.isalnum():
            print(f"{ll}密码只能由数字或字母组成{rr}")
            continue
        ok_passwd = input("请确认密码>>").strip()
        if passwd == ok_passwd:
            result = user.register_api(name, passwd)
            print(result)
            return name
        else:
            print("两次密码不一致,请重新注册")

# 登入功能
def login():
    print(f"{ll}正在登入...{rr}")
    count = 0
    if not login_user["name"] is None:
        print("当前是登入状态,无需登入")
        return
    while 1:
        name = input("请输入用户名(q退出)>>").strip()
        if count == 3:
            common.locker(name)
            print("该用户错误次数过多,已锁定")
            break
        if name.lower() == "q": break
        passwd = input("请输入密码>>").strip()
        tf, result = user.login_api(name, passwd)
        if tf:
            login_user["name"] = name
            print("\n", result)
            break
        else:
            if tf is False:
                count += 1
                print(f"{result},还剩{3 - count}次机会")
            else:
                print(result)

# 取款
@common.login_auth
def withdraw():
    while 1:
        balan = input("请输入取款金额(q退出)>>").strip()
        if balan.lower() == "q": break
        if balan.isdigit():
            balan = int(balan)
            tf, result = bank.withdraw_api(login_user["name"], balan)
            if tf:
                print("\n", result)
                break
            else:
                print(result)
        else:
            print("请输入整数金额")

# 还款
@common.login_auth
def repayment():
    print(f"{ll}正在进入还款操作...{rr}")
    while 1:
        balan = input("请输入还款金额(q退出)>>").strip()
        if balan.lower() == "q": break
        if balan.isdigit():
            balan = int(balan)
            result = bank.repayment_api(login_user["name"], balan)
            print("\n", result)
            break
        else:
            print("请输入整数金额")

# 转账
@common.login_auth
def transfer():
    print(f"{ll}正在进入转账操作...{rr}")
    while True:
        to_name = input('输入转账的用户(q退出)>>:').strip()
        if to_name.lower() == "q": break
        money = input('输入转账金额>>:').strip()
        if money.isdigit():
            money = int(money)
            tf, result = bank.transfer_api(login_user['name'], to_name, money)
            if tf:
                print("\n", result)
                break
            else:
                print(result)
        else:
            print('必须输入数字')

# 查看余额
@common.login_auth
def check_balan():
    print(f"{ll}正在获取账户余额...{rr}\n")
    user_balan = bank.balance_api(login_user["name"])
    print(f"当前账户余额:{llll}￥{user_balan}{rr}")

# 查看个人操作日志(包含流水)
@common.login_auth
def check_account_log():
    log_file = user.user_active(login_user["name"])
    for i in log_file:
        print(f"{llll}{i}{rr}")

# 购物
@common.login_auth
def shopping():
    print(f"{ll}梦想商城欢迎您{rr}\n")
    consume = 0
    user_dic = models.check(login_user["name"])
    user_dic["shops"] = {}
    user_balan = user_dic["balan"]

    while 1:
        print(f'{llll}＊—═—═—═—═—═—═—═—═—═＊{rr}\033[1;32m财富与烟{rr}{llll}＊═—═—═—═—═—═—═—═—═—＊{rr}')
        for k, v in enumerate(shop_dic):
            print(f"   ✿{lll}{k:>3}  goods : {v[0]:<6}  price : {v[1]:<5}{rr}")
        print(f'{llll}━═━═━━═━═━━═━═━═━═━━═━♛━═━━═━═━━═━═━━═━═━━═━═━ {rr}')
        chiose = input("请选择商品编号(q退出)>>").strip()
        if chiose.isdigit():
            chiose = int(chiose)
            if chiose > len(shop_dic) - 1:
                print("未找到此商品")
                continue
            good_name = shop_dic[chiose][0]
            good_price = shop_dic[chiose][1]
            if user_balan >= good_price:
                user_balan -= good_price
                if good_name in user_dic["shops"]:
                    user_dic["shops"][good_name][1] += 1
                    consume += good_price
                else:
                    consume += good_price
                    user_dic["shops"][good_name] = [good_price, 1]
                print(f"商品{ll}{good_name}{rr}已加入购物车")
            else:
                print(f"{ll}信用余额不足!{rr},快去还款款")
        elif chiose.lower() == "q":
            if len(user_dic["shops"]) == 0:
                print(f"{ll}您未购买任何物品{rr}欢迎下次光临!!")
                break
            tf, result = shop.shop_pay(login_user["name"], consume, user_dic)
            if tf:
                print(result)
                break
            elif tf is False:
                print(result)
                break
            else:
                print(result)
                continue
        else:
            print("请输入数字")

# 查看购物车商品
@common.login_auth
def check_shopping_cart():
    user_shops = shop.check_shopping_card(login_user["name"])
    if len(user_shops) == 0:
        print(f"{ll}您什么都没有买{rr}")
    else:
        print(f"{ll}您购买的商品:{rr}")
        for k, v in user_shops.items():
            print(f"{llll}{k:<7}单价:{v[0]:<9}个数:{v[1]:<3}总价:{v[0] * v[1]}元{rr}")

# 管理员入口
def root_login():
    if not login_user["name"] is None:
        print("您当前正在登入,请退出到初始界面进行登入")
        return
    while 1:
        print(f"{ll}管理员登入...{rr}")
        root_name = input("请输入管理员账户(q退出)>>").strip()
        if root_name.lower() == "q": return
        root_passwd = input("请输入管理员密码>>").strip()
        tf, result = root.root_login(root_name, root_passwd)
        if tf:
            print(result)
            root_select()
            break
        else:
            print(result)

## root解锁用户
def root_unlock():
    lock_name = input("请输入需要解锁的用户名>>").strip()
    tf, result = root.unlock_api(lock_name)
    if tf:
        print("\n", result)
        return
    else:
        print(result)

## root锁定用户
def root_lock():
    lock_name = input("请输入需要锁定的用户名>>").strip()
    tf, result = root.lock_api(lock_name)
    if tf:
        print("\n", result)
        return
    else:
        print(result)

## root添加用户
def root_add_user():
    name = root.add_name()
    if name is None:
        pass
    else:
        root.root_loggin.info(f"管理员添加了用户:{name}")

## root删除用户
def root_remove_user():
    name = input("请输入需要删除的账户>>").strip()
    y_n = input(f"{llll}请再次确认Y/其他键取消>>{rr}").strip()
    if y_n.lower() == "y":
        tf, result = root.remove_api(name)
        if tf:
            print("\n", result)
        else:
            print(result)
    else:
        print("您取消了删除用户操作")

## root修改用户额度
def root_change_money():
    name = input("请输入需要更改的额度的账户>>").strip()
    money = input("请输入该用户修改后额度>>").strip()
    if money.isdigit():
        money = int(money)
        tf, result = root.change_api(name, money)
        if tf:
            print("\n", result)
            return
        else:
            print(result)
    else:
        print("请输入整数")

## 查看用户金额流动日志
def check_money_log():
    with open(rf"{setting.transaction_log_file}", "rt", encoding="utf-8")as f:
        for i in f:
            print(f"{lll}{i.strip()}{rr}")

## 查看用户操作日志
def check_operate():
    with open(rf"{setting.login_log_file}", "rt", encoding="utf-8")as f:
        for i in f:
            print(f"{lll}{i.strip()}{rr}")

## 查看管理员日志
def check_root_log():
    with open(rf"{setting.default_log_file}", "rt", encoding="utf-8")as f:
        for i in f:
            print(f"{lll}{i.strip()}{rr}")


# 商场商品菜单
shop_dic = [
    ["私人飞机" , 29988888],
    ["万亩别墅" , 9999999],
    ["劳斯莱斯幻影" , 25555555],
    ["劳力士绿水鬼" , 100000],
    ["私人游艇" , 322000],
    ["哈雷戴维森" , 2000000],
    ["红塔山" , 5],
    ["芙蓉王" , 10],
    ["华子" , 20],
]

# 管理员功能菜单
root_function = [
    ["锁定用户",root_lock],
    ["解锁用户",root_unlock],
    ["添加用户",root_add_user],
    ["删除用户",root_remove_user],
    ["修改用户额度", root_change_money],
    ["查看金额流动日志",check_money_log],
    ["查看用户操作日志",check_operate],
    ["查看管理员日志",check_root_log],
]

# 商场欢迎logo
photo = '''
        ╭╮ ╭╮  ╭──╮  ╭╮    ╭╮    ╭───╮  ╭╮
        ││ ││  │╭─╯  ││    ││    │╭─╮│  ││
        │╰─╯│  │╰╮   ││    ││    ││ ││  ││
        │╭─╮│  │╭╯   ││    ││    ││ ││  ││
        ││ ││  │╰─╮  │╰──╮ │╰──╮ │╰─╯│  ╰╯
        ╰╯ ╰╯  ╰──╯  ╰───╯ ╰───╯ ╰───╯  〇
'''

# atm功能菜单
msg_dic = {
    "0": [logout, "退出登入"],
    "1": [register, "注册"],
    "2": [login, "登入"],
    "3": [withdraw, "取款"],
    "4": [repayment, "还款"],
    "5": [transfer, "转账"],
    "6": [check_balan, "查看余额"],
    "7": [check_account_log, "查看个人流水"],
    "8": [shopping, "购物"],
    "9": [check_shopping_cart, "查看购物车"],
    "10": [root_login, "管理员入口"],
}

# 管理员操作界面
def root_select():
    print(f"\n{ll}欢迎进入管理员界面...{rr}\n")
    while 1:
        print(f'{llll}…·～·…·～·…οΟ○{rr}\033[1;32m权重的力量{rr}{llll}○Οο…·～·…·～·… {rr}')
        for i, v in enumerate(root_function):
            print(f"{'':>10}❖  {lll}{i:<3} {str(v[0]):<5}{rr}")
        print(f'{llll}━━━∞━━━∞━━━∞━━━∞━━🔱━━∞━━━∞━━━∞━━━∞━━━{rr}')
        chiose = input("\n请选择功能(q退出)>>").strip()
        if chiose.lower() == "q":return
        if chiose.isdigit():
            chiose = int(chiose)
            if not chiose >= len(root_function):
                root_function[chiose][1]()
            else:
                print("请输入存在编号")
        else:
            print("请输入数字")


# atm操作总界面
def run():
    print(f"{'':>8}\033[1;30;42m欢迎进入派大星一体式商城,祝您购物愉快\033[0m\n\033[1;32m{photo}\033[0m")
    while 1:
        print(f'{llll}★~☆·☆.~★*∴*~★*∴{rr}\033[1;32m今宵一刻{rr}{llll}*·∴~*★*∴*★~☆·☆.~*∴*~★{rr}')
        for k,v in msg_dic.items():
            print(f"{lll}{'':>15}🔰  {k:<4} {v[1]:<7}{rr}")
        print(f"{lll}{'':>15}🔰  11   退出商城{rr}")
        print(f'{llll}°．·°∴ ☆．．·°．·°∴ ☆．．·°．·°∴ ☆．．·°．·°∴ ☆．·°{rr}')
        count = input("\n请选择服务编号>>").strip()
        if count == "11":
            print("正在退出...\n");break
        if count in msg_dic:
            msg_dic[count][0]()
        else:
            print("请输入存在功能")