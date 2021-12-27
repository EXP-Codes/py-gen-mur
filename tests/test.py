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
from src.scenes import *


class TestPypdmSqlite(unittest.TestCase):

    @classmethod
    def setUpClass(cls) :
        pass


    @classmethod
    def tearDownClass(cls) :
        pass


    def setUp(self) :
        self.REG = Register()
        self.DUUID = self.REG.get_disk_uuid()


    def tearDown(self) :
        pass


    def test_gen_machine_code(self) :
        machine_code = gen_machine_code()
        print(machine_code)
        self.assertEqual(
            self.REG.encrypt_des(self.DUUID), 
            machine_code
        )




if __name__ == '__main__':
    unittest.main()