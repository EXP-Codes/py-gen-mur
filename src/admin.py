#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------

import random
import string
from ._public import *


def read_machine_code() :
    '''
    管理员场景： 读取用户提供的机器码
    [return] 机器码
    '''
    return read(MACHINE_CODE_PATH)


def gen_user_code(bit=8, to_file=True) :
    '''
    管理员场景： 随机分配用户码，并写入文件
    （可直接把文件发送给用户，让其放到程序根目录）
    [param] bit: 用户码位数
    [param] to_file: 是否把用户码写入文件
    [return] 用户码
    '''
    str_range = "%s%s" % (
        string.ascii_letters, 
        string.digits
    )
    user_code = ''.join(
        random.sample(str_range, bit)
    )
    if to_file :
        save(user_code, USER_CODE_PATH)
    return user_code



def gen_register_code(machine_code, user_code, crypt=CRYPT, to_file=True) :
    '''
    管理员场景：
        1. 用户提供 机器码（加密）
        2. 用户预先指定 或 管理员随机分配 的用户码
        3. 用户码（解密） + 机器码 生成 注册码
        4. 注册码写入文件（可直接把文件发送给用户，让其放到程序根目录）
    [param] machine_code: 机器码
    [param] user_code: 用户码
    [param] crypt: 加解密类
    [param] to_file: 是否把机器码写入文件
    [return] 注册码
    '''
    try :
        uuid = crypt.decrypt_des(machine_code)
        register_code = gen_rc(crypt, uuid, user_code)
    except :
        register_code = ''
    if to_file :
        save(register_code, REGISTER_CODE_PATH)
    return register_code

