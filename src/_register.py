#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------
'''
原理
    1. 判断路径下是否存在识别文件，若存在就解密对比，若不存在就进入机器码注册：
    2. 获取系统C盘序列号作为识别ID，并添加随机数作为混淆，生成最终机器码。
    3. 将机器码发给软件开发者，开发者将机器码解密后，添加自己的标识符号并加密生成key，发给用户。
    4. 用户输入key，程序对比并保存。
    5. 用户下次打开软件时，重新开始步骤‘1’。
说明
    1. 加密：将序列号经过Des加密，再经过base64编码。
    2. 解密：将密码经过base64解码，再经过Des解密。
    3. 写文件：将二进制字符转为十六进制保存。
    4. 读文件：将十六进制转为二进制。
'''

import base64
import win32api
from pyDes import *

class Register:

    def __init__(self, key=None, iv=None):
        # FIXME 提供随机生成的方法
        self.des_key = key or b"FV>0Y_:D"                           # DES 加解密 Key
        self.des_iv = iv or b"\x34\x6A\x52\xBC\x37\x2D\x36\xEF"     # 初始 IV 向量（盐）
        self.des_obj = des(self.des_key, CBC, self.des_iv, pad=None, padmode=PAD_PKCS5)
    

    def get_disk_uuid(self):
        '''
        获取硬盘唯一标识。
        tuple = win32api.GetVolumeInformation(path)

            Parameters
                path : string
                        The root path of the volume on which information is being requested.
            Return Value
                The return is a tuple of:
                    string - Volume Name
                    long - Volume serial number.
                    long - Maximum Component Length of a file name.
                    long - Sys Flags - other flags specific to the file system. See the api for details.
                    string - File System Name
        '''
        disk_infos = win32api.GetVolumeInformation("C:\\")
        s_disk_infos = list(map(lambda e: str(e), disk_infos))
        return ';'.join(s_disk_infos[1:])   # 排除最容易修改的分卷名，其他参数除非格盘或重装系统，否则难以改变


    def encrypt_des(self, plaintext):
        '''
        DES 加密
        '''
        byte_ciphertext = base64.b64encode(self.des_obj.encrypt(plaintext))
        return self.byte_to_str(byte_ciphertext)
    

    def decrypt_des(self, ciphertext):
        '''
        DES 解密
        '''
        byte_plaintext = self.des_obj.decrypt(base64.b64decode(ciphertext))
        return self.byte_to_str(byte_plaintext)
    

    #获取注册码，验证成功后生成注册文件
    def regist(self):
        key = input('please input your register code: ')
        #由于输入类似“12”这种不符合base64规则的字符串会引起异常，所以需要增加输入判断
        #while key
        if key:
            content = self.get_disk_uuid()   # number has been changed to str type after use str()
            key_decrypted=self.decrypt_des(key)
            if content!=0 and key_decrypted!=0:
                if content != key_decrypted:
                    print("wrong register code, please check and input your register code again:")
                    self.regist()
                elif content==key_decrypted:
                    print("register succeed.")
                    #读写文件要加判断
                    with open('./register','w') as f:
                        f.write(key)
                        f.close()
                    return True
                else:
                    return False
            else:
                return False
        else:
            self.regist()
        return False

    def check_authored(self):
        content=self.get_disk_uuid()
        check_authoredResult = 0
        #读写文件要加判断
        try:
            f=open('./register','r')
            if f:
                    key=f.read()
                    if key:
                        key_decrypted=self.decrypt_des(key)
                        if key_decrypted:
                            if key_decrypted == content:
                                check_authoredResult = 1
                            else:
                                check_authoredResult = -1
                        else:
                            check_authoredResult = -2
                    else:
                        check_authoredResult = -3
            else:
                self.regist()
        except IOError:
            print(IOError)
        print(check_authoredResult)
        return check_authoredResult

    def byte_to_str(self, value) :
        """
        byte 转 str。
        sqlite 入库类型为 TEXT 的数据会自动转为 byte，读取时要先转回来。
        :param value: byte 值
        :return: str 字符串
        """
        if isinstance(value, bytes) :
            value = bytes.decode(value)
        return value


if __name__ == '__main__':
    reg=Register()
    # reg.regist()


    # 1. 用户运行 reg.encrypt_des(reg.get_disk_uuid()) 加密的获得机器码
    # 2. 开发者
    # print(reg.encrypt_des(reg.get_disk_uuid()))

    reg.check_authored()
