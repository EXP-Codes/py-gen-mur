#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------

import os
import random
import string
from ._crypt import Crypt
from ._mi import MachineInfo

MACHINE_CODE_PATH = './.machine'
USER_CODE_PATH = './.user'
REGISTER_CODE_PATH = './.register'

CRYPT = Crypt()
MI = MachineInfo()


def gen_machine_code(crypt=CRYPT, to_file=True) :
    '''
    用户场景： 生成机器码
    '''
    uuid = MI.generate()
    machine_code = crypt.encrypt_des(uuid)
    if to_file :
        _save(machine_code, MACHINE_CODE_PATH)
    return machine_code


def gen_user_code(bit=8, to_file=True) :
    '''
    管理员场景： 分配随机用户码（盐）
    '''
    str_range = "%s%s" % (
        string.ascii_letters, 
        string.digits
    )
    user_code = ''.join(
        random.sample(str_range, bit)
    )
    if to_file :
        _save(user_code, USER_CODE_PATH)
    return user_code


def gen_register_code(machine_code, user_code, crypt=CRYPT, to_file=True) :
    '''
    管理员场景： 混合机器码与用户码，生成注册码
    '''
    try :
        uuid = crypt.decrypt_des(machine_code)
        register_code = _gen_rc(crypt, uuid, user_code)
    except :
        register_code = ''
    if to_file :
        _save(register_code, REGISTER_CODE_PATH)
    return register_code


def verify_authorization(user_code, crypt=CRYPT) :
    '''
    用户场景： 每次运行程序时，输入用户码； 校验【机器码+用户码=注册码】
    '''
    uuid = MI.generate()
    register_code = _gen_rc(crypt, uuid, user_code)
    return register_code == _read(REGISTER_CODE_PATH)


def _gen_rc(crypt, uuid, user_code) :
    return crypt.to_md5(
        crypt.encrypt_des(
            "%s##%s" % (user_code, uuid)
        )
    )


def _save(code, filepath) :
    '''
    保存
    '''
    with open(filepath, 'w+') as file :
        file.write(code)


def _read(filepath) :
    '''
    读取
    '''
    code = ''
    if os.path.exists(filepath) :
        with open(filepath, 'r') as file :
            code = file.read()
    return code


