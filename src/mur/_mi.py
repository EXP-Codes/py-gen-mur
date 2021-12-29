#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------

import platform
from psutil import net_if_addrs
from datetime import datetime


class MachineInfo :

    def __init__(self) -> None:
        if self._is_windows() :
            import win32api


    def generate(self) :
        mc = '\n'.join([
            self._get_disk_uuid(), 
            self._get_net_uuid()
            # TODO 可以添加其他机器标识
        ])
        return mc


    def _get_disk_uuid(self):
        uuid = ''
        if self._is_windows() :
            uuid = self._get_win_disk_uuid()

        else :
            uuid = self._get_linux_disk_uuid()
        return uuid


    def _get_win_disk_uuid(self):
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


    def _get_linux_disk_uuid(self):
        # TODO 因权限问题、或受限于系统组件，尚未有较好方法获取硬盘唯一标识
        return ''


    def _get_net_uuid(self):
        uuid = ''
        if self._is_windows() :
            uuid = self._get_win_net_uuid()

        else :
            uuid = self._get_linux_net_uuid()
        return uuid

    
    def _get_win_net_uuid(self):
        # FIXME win 网卡比较容易改变（例如安装虚拟机等都会新增网卡），暂不纳入标识
        return ''


    def _get_linux_net_uuid(self):
        '''
        获取网卡唯一标识（MAC 地址）
        '''
        macs = []
        for k, v in net_if_addrs().items():
            for item in v:
                address = item[1]
                if len(address) != 17 :
                    continue
                if ('-' in address) or (':' in address) :
                    macs.append(address)
        return ';'.join(macs)


    def _os(self) :
        return platform.system()


    def _is_windows(self) :
        return self._os() == 'Windows'


    def _is_mac(self) :
        return self._os() == 'Darwin'


    def _is_linux(self) :
        return self._os() == 'Linux'

