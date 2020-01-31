import psutil

from typing import List


class TopProcess:
    MAX_OUTPUT = 10

    @classmethod
    def _get_process_list(cls) -> List[dict]:
        proc_list = []

        for proc in psutil.process_iter():
            try:
                info = proc.as_dict(attrs=['pid', 'name', 'cpu_percent'])
                info['vms'] = proc.memory_info().vms
                proc_list.append(info)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        return proc_list

    @classmethod
    def cpu_sorted(cls) -> List[dict]:
        s = sorted(cls._get_process_list(), key=lambda x: x['cpu_percent'], reverse=True)
        i = min(len(s), cls.MAX_OUTPUT)
        return s[0: i]

    @classmethod
    def mem_sorted(cls) -> List[dict]:
        s = sorted(cls._get_process_list(), key=lambda x: x['vms'], reverse=True)
        i = min(len(s), cls.MAX_OUTPUT)
        return s[0: i]
