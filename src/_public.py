#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------

import os
from ._crypt import Crypt
from ._mi import MachineInfo

# 因代码开源，不建议 Crypt 使用默认类。建议使用此工具时，自定义指定 Crypt 构造函数的 key 和 iv
# 在 _crypt 提供了生成随机 key 和 iv 的方法
# 但是生成后必须另外存储这两值，否则之前使用其生成的注册码无法再解密
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


