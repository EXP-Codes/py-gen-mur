#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------

import platform
import win32api
import psutil
from datetime import datetime


class MachineInfo :

    def __init__(self) -> None:
        pass


    def generate(self) :
        mc = '\n'.join([
            self._get_disk_uuid(), 
            # TODO 
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
        # TODO
        return ''
    

    def _os(self) :
        return platform.system()


    def _is_windows(self) :
        return self._os() == 'Windows'


    def _is_mac(self) :
        return self._os() == 'Darwin'


    def _is_linux(self) :
        return self._os() == 'Linux'

