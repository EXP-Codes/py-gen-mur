#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------

import os
import random
import string
from ._crypt import *
from ._mi import MachineInfo

MACHINE_CODE_PATH = './.machine'
USER_CODE_PATH = './.user'
REGISTER_CODE_PATH = './.register'


# 因代码开源，不建议 Crypt 使用默认类。建议使用此工具时，自定义指定 Crypt 构造函数的 key 和 iv
# 在 _crypt 提供了生成随机 key 和 iv 的方法
# 但是生成后必须另外存储这两值，否则之前使用其生成的注册码无法再解密
CRYPT = Crypt()     
MI = MachineInfo()


def gen_machine_code(crypt=CRYPT, to_file=True) :
    '''
    用户场景： 生成机器码，并写入文件
    （可直接把文件发送给管理员，让其生成注册码）
    [param] crypt: 加解密类
    [param] to_file: 是否把用户码写入文件
    [return] 用户码
    '''
    uuid = MI.generate()
    machine_code = crypt.encrypt_des(uuid)
    if to_file :
        _save(machine_code, MACHINE_CODE_PATH)
    return machine_code


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
        _save(user_code, USER_CODE_PATH)
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
        register_code = _gen_rc(crypt, uuid, user_code)
    except :
        register_code = ''
    if to_file :
        _save(register_code, REGISTER_CODE_PATH)
    return register_code


def verify_authorization(user_code, crypt=CRYPT) :
    '''
    用户场景： 每次运行程序时，
        1. 输入用户码 
        2. 获取机器码
        3. 用户码 + 机器码 生成 注册码
        4. 读取管理员提供的 注册码
        5. 比较两个注册码是否相同
    [param] user_code: 用户码
    [param] crypt: 加解密类
    [return] true: 注册码一致； false: 注册码不同
    '''
    uuid = MI.generate()
    register_code = _gen_rc(crypt, uuid, user_code)
    return register_code == _read(REGISTER_CODE_PATH)


def _gen_rc(crypt, uuid, user_code) :
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


def _save(code, filepath) :
    '''
    保存 xx码
    [param] code: xx码
    [param] filepath: 保存位置
    [return] xx码
    '''
    with open(filepath, 'w+') as file :
        file.write(code)
    return code


def _read(filepath) :
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


