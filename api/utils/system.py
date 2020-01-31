import time
import psutil
from typing import List

from .common import find_line, find_value


class SystemInfo:
    RPI_FILE = '/proc/device-tree/model'
    CPU_FILE = '/proc/cpuinfo'
    DIST_FILE = '/etc/os-release'

    RPI_ERR = 'NOT a RPi System.'
    CPU_ERR = 'Unavailable'
    DIST_ERR = 'Unavailable'

    @classmethod
    def rpi(cls) -> str:
        try:
            with open(cls.RPI_FILE, 'r') as f:
                return f.readline()
        except OSError:
            return cls.RPI_ERR

    @classmethod
    def cpu(cls) -> str:
        try:
            with open(cls.CPU_FILE, 'r') as f:
                return find_value(find_line(f.readlines(), 'model name', cls.CPU_ERR), ':')
        except OSError:
            return cls.CPU_ERR

    @classmethod
    def total_mem(cls) -> int:
        return psutil.virtual_memory().total

    @classmethod
    def dist(cls) -> str:
        try:
            with open(cls.DIST_FILE, 'r') as f:
                return find_value(find_line(f.readlines(), 'PRETTY_NAME', cls.DIST_ERR), '=')\
                    .replace('"', '')
        except OSError:
            return cls.DIST_ERR

    @classmethod
    def serialize(cls) -> dict:
        return {
            'rpi': cls.rpi(),
            'cpu': cls.cpu(),
            'total_mem': cls.total_mem(),
            'dist': cls.dist()
        }


class SystemStatus:
    TEMP_FILE = '/sys/class/thermal/thermal_zone{}/temp'
    MAXIMUM_CORE = 16

    @classmethod
    def using_mem(cls) -> int:
        return psutil.virtual_memory().used

    @classmethod
    def num_proc(cls) -> int:
        return len(psutil.pids())

    @classmethod
    def temperature(cls) -> List[float]:
        temp_list = []
        try:
            for i in range(cls.MAXIMUM_CORE):
                with open(cls.TEMP_FILE.format(i), 'r') as f:
                    temp_list.append(int(f.readline()) / 1000.0)
        except OSError:
            pass

        return temp_list

    @classmethod
    def current_time(cls) -> str:
        return time.strftime('%c')

    @classmethod
    def serialize(cls) -> dict:
        return {
            'using_mem': cls.using_mem(),
            'num_proc': cls.num_proc(),
            'temperature': cls.temperature(),
            'current_time': cls.current_time()
        }
