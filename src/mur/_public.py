#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------

import os
import time
import requests
import json
from .crypt import Crypt
from ._mi import MachineInfo

CRYPT = Crypt()     
MI = MachineInfo()

JOINER = '##'
ONLINE_TIME_URL = 'http://api.m.taobao.com/rest/api3.do?api=mtop.common.getTimestamp'
UNLIMIT = '0000000000'

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


def now() :
    '''
    获取当前时间点（精确到秒）
    [return] 当前时间戳（long）
    '''
    try :
        # 先获取在线时间，避免用户修改本地时间绕过注册校验
        response = requests.get(ONLINE_TIME_URL, verify=False, timeout=10)
        millis = int(json.loads(response.text)['data']['t'])
        seconds = int(millis / 1000)
    except :
        # 网络不通时用本地时间代替
        seconds = int(time.time())
    return seconds


def after(days) :
    '''
    获取今天之后的 n 天的时间点（精确到秒）
    [param] days: 之后的 n 天
    [return] n 天后的时间戳（str）
    '''
    timestamp = UNLIMIT
    if days > 0 :
        seconds = days * 86400
        timestamp = now() + seconds
    return str(timestamp)



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
        parent_filepath = "../%s" % os.path.basename(filepath)
        if os.path.exists(parent_filepath) :
            with open(parent_filepath, 'r') as file :
                code = file.read()
    return code


