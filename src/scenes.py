#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------

import random
import string
from ._register import Register

JOINER = '##'


def gen_machine_code() :
    '''
    用户场景： 生成机器码
    '''
    reg = Register()
    dsn = reg.get_disk_serial_number()
    machine_code = reg.encrypt_des(dsn)
    return machine_code


def gen_user_code(bit=8) :
    '''
    管理员场景： 分配随机用户码（盐）
    '''
    str_range = string.ascii_letters + string.digits
    user_code = ''.join(random.sample(str_range, bit))
    return user_code


def gen_register_code(machine_code, user_code) :
    '''
    管理员场景： 混合机器码与用户码，生成注册码
    '''
    reg = Register()
    try :
        dsn = reg.decrypt_des(machine_code)
        rc = _gen_rc(reg, dsn, user_code)
    except :
        rc = ''
    return rc


def _gen_rc(reg, dsn, user_code) :
    return reg.encrypt_des("%s%s%s" % (user_code, JOINER, dsn))



def verify_authorization(user_code) :
    '''
    用户场景： 每次运行程序时，输入用户码； 校验【机器码+用户码=注册码】
    '''
    reg = Register()
    dsn = reg.get_disk_serial_number()
    rc = _gen_rc(reg, dsn, user_code)
    return rc == read_register_code()



def save_register_code(register_code) :
    '''
    用户场景： 保存注册码到本地
    '''
    pass
    # TODO


def read_register_code() :
    '''
    用户场景： 读取本地注册码
    '''
    register_code = ''
    # TODO
    return register_code

    
