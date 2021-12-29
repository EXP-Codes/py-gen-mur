#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------
# 为用户生成【用户码】和【注册码】
# 注意：
#   .des_key 和 .des_iv 需要保管好，不能泄露
# -----------------------------------------------

from src.mur.crypt import *
from src.mur.admin import *

DES_KEY_PATH = '.des_key'
DES_IV_PATH = '.des_iv'


def main() :
    machine_code = read_machine_code() 
    if is_empty(machine_code) :
        print('找不到【机器码】')
        print('请把用户提供的【%s】文件复制到根目录' % MACHINE_CODE_PATH)
    else :
        des_key = read_des_key()
        des_iv = read_des_iv()
        crypt = Crypt(des_key, des_iv)

        user_code = gen_user_code()
        print('随机分配的【用户码】为 [%s]' % user_code)
        print('已把【用户码】保存到根目录的文件 [%s]，请把该文件发送给用户' % USER_CODE_PATH)

        register_code = gen_register_code(
            machine_code, user_code, crypt
        )
        print('为用户生成的【注册码】为 [%s]' % register_code)
        print('已把【注册码】保存到根目录的文件 [%s]，请把该文件发送给用户' % REGISTER_CODE_PATH)



def read_des_key() :
    '''
    从文件读取 DES Key。
    若文件不存在，则生成一个（需要妥善保管好）。
    '''
    des_key = read(DES_KEY_PATH)
    if is_empty(des_key) :
        des_key = gen_des_key()
        save(b2s(des_key), DES_KEY_PATH)
    return des_key


def read_des_iv() :
    '''
    从文件读取 DES IV。
    若文件不存在，则生成一个（需要妥善保管好）。
    '''
    des_iv = read(DES_IV_PATH)
    if is_empty(des_iv) :
        des_iv = gen_des_key()
        save(b2s(des_iv), DES_IV_PATH)
    return s2b(des_iv)


def is_empty(str) :
    return str is None or str == ''


if __name__ == '__main__':
    main()
