#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------

import os
from .crypt import Crypt
from ._mi import MachineInfo

CRYPT = Crypt()     
MI = MachineInfo()

MACHINE_CODE_PATH = './.machine'
USER_CODE_PATH = './.user'
REGISTER_CODE_PATH = './.register'
CODE_PATHS = [ 
    MACHINE_CODE_PATH, 
    USER_CODE_PATH, 
    REGISTER_CODE_PATH 
]


def gen_rc(crypt, uuid, user_code) :
    '''
    生成注册码
    [param] crypt: 加解密类
    [param] uuid: 用户机器唯一表示
    [param] user_code: 用户码
    [return] 注册码
    '''
    return crypt.to_md5(
        crypt.encrypt_des(
            "%s##%s" % (user_code, uuid)
        )
    )


def save(code, filepath) :
    '''
    保存 xx码
    [param] code: xx码
    [param] filepath: 保存位置
    [return] xx码
    '''
    with open(filepath, 'w+') as file :
        file.write(code)
    return code


def read(filepath) :
    '''
    读取 xx码
    [param] filepath: 保存位置
    [return] xx码
    '''
    code = ''
    if os.path.exists(filepath) :
        with open(filepath, 'r') as file :
            code = file.read()
    return code


