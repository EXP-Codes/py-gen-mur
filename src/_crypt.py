#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------

import hashlib
import base64
from pyDes import *
import binascii

class Crypt:

    def __init__(self, key=None, iv=None):
        # FIXME 提供随机生成的方法
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
        ciphertext = self._b2s(_hex)                # 16进制字节 转为 16进制字符串
        return ciphertext.upper()                   # 字符串大写
    

    def decrypt_des(self, ciphertext):
        '''
        DES 解密
        '''
        _hex = self._s2b(ciphertext)                # 字符串 还原为 16进制字节
        _base64 = binascii.a2b_hex(_hex)            # 16进制字节 还原为 Base64
        _des = base64.b64decode(_base64)            # Base64 还原为 DES密文
        plaintext = self.des_obj.decrypt(_des)      # DES密文 解密为 明文字节
        return self._b2s(plaintext)                 # 明文字节 转为 明文字符串
    
    
    def to_md5(self, text) :
        '''
        生成 MD5
        '''
        return hashlib.md5(
            self._s2b(text)
        ).hexdigest().upper()


    def _b2s(self, value) :
        """
        byte 转 str。
        :param value: byte 值
        :return: str 字符串
        """
        if isinstance(value, bytes) :
            value = bytes.decode(value)
        return value


    def _s2b(self, value) :
        """
        str 转 byte。
        :param value: str 字符串
        :return: byte 值
        """
        if isinstance(value, str) :
            value = str.encode(value)
        return value

