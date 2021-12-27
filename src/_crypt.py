#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------

import random
import string
import hashlib
import base64
from pyDes import *
import binascii


def gen_des_key() :
    '''
    生成 DES Key 、
    **生成后需注意自行保存，不要丢失**
    [return] DES Key
    '''
    des_key = _gen_random_bytes()
    print("DES Key: %s" % des_key)
    return des_key


def gen_des_iv() :
    '''
    生成 DES IV （初始向量）。
    **生成后需注意自行保存，不要丢失**
    [return] DES IV
    '''
    des_iv = _gen_random_bytes()
    print("DES IV: %s" % des_iv)
    return des_iv


def _gen_random_bytes() :
    '''
    生成 8 bit 的随机字节
    [return] 8 bit 随机字节
    '''
    str_range = "%s%s" % (string.ascii_letters, string.digits)
    return _s2b(''.join(random.sample(str_range, 8)))


def _b2s(value) :
    '''
    byte 转 str。
    [param] value: byte 字节
    [return] str 字符串
    '''
    if isinstance(value, bytes) :
        value = bytes.decode(value)
    return value


def _s2b(value) :
    '''
    str 转 byte。
    [param] str 字符串
    [return] byte 字节
    '''
    if isinstance(value, str) :
        value = str.encode(value)
    return value

        

class Crypt:

    def __init__(self, key=None, iv=None):
        self.des_key = key or b"FV>0Y_:D"                           # DES 加解密 Key
        self.des_iv = iv or b"\x34\x6A\x52\xBC\x37\x2D\x36\xEF"     # 初始 IV 向量（盐）
        self.des_obj = des(self.des_key, CBC, self.des_iv, pad=None, padmode=PAD_PKCS5)


    def encrypt_des(self, plaintext):
        '''
        DES 加密
        '''
        _des = self.des_obj.encrypt(plaintext)      # DES 加密
        _base64 = base64.b64encode(_des)            # DES密文 转为 Base64
        _hex = binascii.b2a_hex(_base64)            # Base64 转为 16进制字节
        ciphertext = _b2s(_hex)                     # 16进制字节 转为 16进制字符串
        return ciphertext.upper()                   # 字符串大写
    

    def decrypt_des(self, ciphertext):
        '''
        DES 解密
        '''
        _hex = _s2b(ciphertext)                     # 字符串 还原为 16进制字节
        _base64 = binascii.a2b_hex(_hex)            # 16进制字节 还原为 Base64
        _des = base64.b64decode(_base64)            # Base64 还原为 DES密文
        plaintext = self.des_obj.decrypt(_des)      # DES密文 解密为 明文字节
        return _b2s(plaintext)                      # 明文字节 转为 明文字符串
    
    
    def to_md5(self, text) :
        '''
        生成 MD5
        '''
        return hashlib.md5(
            _s2b(text)
        ).hexdigest().upper()


    

