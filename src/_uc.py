#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------

import random
import string


class UserCode :

    def __init__(self) -> None:
        pass



    def generate(self, bit=8) :
        '''
        管理员场景： 分配随机用户码（盐）
        '''
        str_range = string.ascii_letters + string.digits
        user_code = ''.join(random.sample(str_range, bit))
        return user_code