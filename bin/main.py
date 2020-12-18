'''
程序入口
'''


import os
import sys
from core import src

# 将执行文件所在的目录加入环境变量中
sys.path.append(os.path.dirname(os.path.dirname(__file__)))


if __name__ == '__main__':
    pass
src.run()