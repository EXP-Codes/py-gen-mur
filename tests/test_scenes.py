#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package
# ----------------------------------------------------------------------
# 把父级目录（项目根目录）添加到工作路径，以便在终端也可以执行单元测试
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
# ----------------------------------------------------------------------

import unittest
from src._crypt import *
from src.scenes import *


class TestScenes(unittest.TestCase):

    @classmethod
    def setUpClass(cls) :
        pass


    @classmethod
    def tearDownClass(cls) :
        pass


    def setUp(self) :
        self.CRYPT = Crypt()
        self.MI = MachineInfo()
        self.UUID = self.MI.generate()


    def tearDown(self) :
        pass


    def test_des(self) :
        print("机器唯一标识： %s" % self.UUID)
        ciphertext = self.CRYPT.encrypt_des(self.UUID)
        print("机器码（密文）： %s" % ciphertext)
        plaintext = self.CRYPT.decrypt_des(ciphertext)
        print("机器码（明文）： %s" % plaintext)
        self.assertEqual(
            plaintext, 
            self.UUID
        )


    def test_gen_machine_code(self) :
        machine_code = gen_machine_code()
        print("机器码： %s" % machine_code)
        self.assertEqual(
            self.CRYPT.encrypt_des(self.UUID), 
            machine_code
        )


    def test_gen_user_code(self) :
        BIT = 16
        user_code = gen_user_code(BIT)
        print("用户码： %s" % user_code)
        self.assertEqual(
            len(user_code), 
            BIT
        )
    

    def test_gen_register_code(self) :
        my_key = gen_des_key()  # 注意自行生成的 key 需要保存好
        my_iv = gen_des_iv()    # 注意自行生成的 iv 需要保存好
        my_crypt = Crypt(key=my_key, iv=my_iv)  # 使用自己的 key 和 iv 构造加解密类，就不怕开源复用了

        machine_code = gen_machine_code(my_crypt)
        print("机器码： %s" % machine_code)
        user_code = gen_user_code()
        print("用户码： %s" % user_code)
        register_code = gen_register_code(machine_code, user_code, my_crypt)
        print("注册码： %s" % register_code)
        self.assertRegex(
            register_code, 
            r"[0-9A-Z]{32,32}"
        )


    def test_verify_authorization(self) :
        user_code = "U32zH48k"              # 用户预先指定 或 管理员随机分配 的用户码
        machine_code = gen_machine_code()   # 用户提供的机器码（这行代码在用户本地执行）
        gen_register_code(machine_code, user_code)  # 管理员为用户生成的注册码（这行代码在管理员本地执行）

        # ...
        # 用户把管理员提供的注册码，放到本地指定位置的文件
        # ...

        # 这行代码在用户本地执行，主要做三件事：
        #   1. 接受用户输入的 用户码
        #   2. 在用户本地重新生成机器码
        #   3. 利用 用户码 和 机器码 生成 注册码
        #   4. 比对 生成的注册码 和 用户放到本地的注册码文件内容 是否一致
        rst = verify_authorization(user_code)
        self.assertTrue(rst)









if __name__ == '__main__':
    unittest.main()