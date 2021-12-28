#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------

import random
import string


def gen_random_bytes() :
    '''
    生成 8 bit 的随机字节
    [return] 8 bit 随机字节
    '''
    str_range = "%s%s" % (string.ascii_letters, string.digits)
    return s2b(''.join(random.sample(str_range, 8)))


def b2s(value) :
    '''
    byte 转 str。
    [param] value: byte 字节
    [return] str 字符串
    '''
    if isinstance(value, bytes) :
        value = bytes.decode(value)
    return value


def s2b(value) :
    '''
    str 转 byte。
    [param] str 字符串
    [return] byte 字节
    '''
    if isinstance(value, str) :
        value = str.encode(value)
    return value
