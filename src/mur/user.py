#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------

from ._public import *


def gen_machine_code(crypt=CRYPT, to_file=True) :
    '''
    用户场景： 生成机器码，并写入文件
    （可直接把文件发送给管理员，让其生成注册码）
    [param] crypt: 加解密类
    [param] to_file: 是否把用户码写入文件
    [return] 机器码码
    '''
    uuid = MI.generate()
    machine_code = crypt.encrypt_des(uuid)
    if to_file :
        save(machine_code, MACHINE_CODE_PATH)
    return machine_code


def read_user_code() :
    '''
    用户场景： 读取（或输入）被管理员分配的用户码
    [return] 用户码
    '''
    user_code = read(USER_CODE_PATH)   # 若无法从文件中读取
    if user_code == '' :
        user_code = input('请输入用户码: ')   # 则要求用户输入
    return user_code


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
    rst = False
    try :
        uuid = MI.generate()
        expire_time = crypt.decrypt_des(user_code)
        register_code = gen_rc(crypt, uuid, expire_time)
        rst = (register_code == read(REGISTER_CODE_PATH))
        if rst :
            expire_time = int(expire_time)
            expire_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(expire_time))
            if expire_time == 0 :
                print('注册码正确（永久）。')

            elif now() <= expire_time :
                print('注册码正确（有效期至 %s）。' % expire_date)
            else :
                rst = False
                print('注册码已过期（有效期至 %s）。' % expire_date)
    except :
        pass
    if not rst :
        print('用户码错误 或 注册码不存在，请联系管理员。')
    return rst
