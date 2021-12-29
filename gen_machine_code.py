#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------
# 请把此代码复制到被注入的程序，由用户执行生成【机器码】
# 注意：
#   des_key 和 des_iv 的值需要手动改为与注册机一致
# -----------------------------------------------

from mur.crypt import *
from mur.user import *


def main() :
    des_key = 'FIXME'   # 需要手动修改为与注册机 gen_register_code.py 一样的值
    des_iv = 'FIXME'    # 需要手动修改为与注册机 gen_register_code.py 一样的值
    crypt = Crypt(des_key, des_iv)

    machine_code = gen_machine_code(crypt)
    print('已生成机器码 [%s]' % machine_code)
    print('已生成机器码对应的本地文件 [%s]' % MACHINE_CODE_PATH)
    print('请将其发送给管理员，以获取注册码。')


if __name__ == '__main__':
    main()


