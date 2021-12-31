#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------

import os
import time
from .crypt import Crypt
from ._mi import MachineInfo

CRYPT = Crypt()     
MI = MachineInfo()

JOINER = '##'
MACHINE_CODE_PATH = '.machine'
USER_CODE_PATH = '.user'
REGISTER_CODE_PATH = '.register'
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
            "%s%s%s" % (user_code, JOINER, uuid)
        )
    )


def after(days) :
    '''
    获取今天之后的 n 天的时间点（精确到秒）
    [param] days: 之后的 n 天
    [return] n 天后的 long 时间戳
    '''
    days = 0 if days <= 0 else days
    seconds = days * 86400
    now = time.time()
    return now + seconds


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

    # 若当前目录读取不到，则试图从上级目录读取
    # 用于使用 pyinstaller 发布后，需要创建“快捷方式”或“软链”到上层目录的场景
    else :
        parent_filepath = os.path.dirname(os.path.abspath(filepath))
        if os.path.exists(parent_filepath) :
            with open(parent_filepath, 'r') as file :
                code = file.read()
    return code


