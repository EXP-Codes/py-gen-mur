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
        print("="*40, "System Information", "="*40)
        uname = platform.uname()
        print(f"System: {uname.system}")
        print(f"Node Name: {uname.node}")
        print(f"Release: {uname.release}")
        print(f"Version: {uname.version}")
        print(f"Machine: {uname.machine}")
        print(f"Processor: {uname.processor}")
        # Boot Time
        print("="*40, "Boot Time", "="*40)
        boot_time_timestamp = psutil.boot_time()
        bt = datetime.fromtimestamp(boot_time_timestamp)
        print(f"Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}")
        # let's print CPU information
        print("="*40, "CPU Info", "="*40)
        # number of cores
        print("Physical cores:", psutil.cpu_count(logical=False))
        print("Total cores:", psutil.cpu_count(logical=True))
        # CPU frequencies
        cpufreq = psutil.cpu_freq()
        print(f"Max Frequency: {cpufreq.max:.2f}Mhz")
        print(f"Min Frequency: {cpufreq.min:.2f}Mhz")
        print(f"Current Frequency: {cpufreq.current:.2f}Mhz")
        # CPU usage
        print("CPU Usage Per Core:")
        for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
            print(f"Core {i}: {percentage}%")
        print(f"Total CPU Usage: {psutil.cpu_percent()}%")
        # Memory Information
        print("="*40, "Memory Information", "="*40)
        # get the memory details
        svmem = psutil.virtual_memory()
        print(f"Total: {self._get_size(svmem.total)}")
        print(f"Available: {self._get_size(svmem.available)}")
        print(f"Used: {self._get_size(svmem.used)}")
        print(f"Percentage: {svmem.percent}%")
        print("="*20, "SWAP", "="*20)
        # get the swap memory details (if exists)
        swap = psutil.swap_memory()
        print(f"Total: {self._get_size(swap.total)}")
        print(f"Free: {self._get_size(swap.free)}")
        print(f"Used: {self._get_size(swap.used)}")
        print(f"Percentage: {swap.percent}%")
        # Disk Information
        print("="*40, "Disk Information", "="*40)
        print("Partitions and Usage:")
        # get all disk partitions
        partitions = psutil.disk_partitions()
        for partition in partitions:
            print(f"=== Device: {partition.device} ===")
            print(f"  Mountpoint: {partition.mountpoint}")
            print(f"  File system type: {partition.fstype}")
            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
            except PermissionError:
                # this can be catched due to the disk that
                # isn't ready
                continue
            print(f"  Total Size: {self._get_size(partition_usage.total)}")
            print(f"  Used: {self._get_size(partition_usage.used)}")
            print(f"  Free: {self._get_size(partition_usage.free)}")
            print(f"  Percentage: {partition_usage.percent}%")
        # get IO statistics since boot
        disk_io = psutil.disk_io_counters()
        print(f"Total read: {self._get_size(disk_io.read_bytes)}")
        print(f"Total write: {self._get_size(disk_io.write_bytes)}")
        # Network information
        print("="*40, "Network Information", "="*40)
        # get all network interfaces (virtual and physical)
        if_addrs = psutil.net_if_addrs()
        for interface_name, interface_addresses in if_addrs.items():
            for address in interface_addresses:
                print(f"=== Interface: {interface_name} ===")
                if str(address.family) == 'AddressFamily.AF_INET':
                    print(f"  IP Address: {address.address}")
                    print(f"  Netmask: {address.netmask}")
                    print(f"  Broadcast IP: {address.broadcast}")
                elif str(address.family) == 'AddressFamily.AF_PACKET':
                    print(f"  MAC Address: {address.address}")
                    print(f"  Netmask: {address.netmask}")
                    print(f"  Broadcast MAC: {address.broadcast}")
        # get IO statistics since boot
        net_io = psutil.net_io_counters()
        print(f"Total Bytes Sent: {self._get_size(net_io.bytes_sent)}")
        print(f"Total Bytes Received: {self._get_size(net_io.bytes_recv)}")
        return ''
    

    def _get_size(bytes, suffix="B"):
        """
        Scale bytes to its proper format
        e.g:
            1253656 => '1.20MB'
            1253656678 => '1.17GB'
        """
        factor = 1024
        for unit in ["", "K", "M", "G", "T", "P"]:
            if bytes < factor:
                return f"{bytes:.2f}{unit}{suffix}"
            bytes /= factor


    def _os(self) :
        return platform.system()


    def _is_windows(self) :
        return self._os() == 'Windows'


    def _is_mac(self) :
        return self._os() == 'Darwin'


    def _is_linux(self) :
        return self._os() == 'Linux'

