from typing import List
from typing_extensions import TypedDict


class FileType(TypedDict):
    name: str
    is_dir: bool
    created: str
    modified: str
    size: int


class PinType(TypedDict):
    pin: int
    type: str
    mode: int
    value: int
    pwm: bool
    pwm_freq: int
    pwm_dutycycle: int


class ProcType(TypedDict):
    pid: int
    name: str
    cpu_percent: float
    vms: int


class SystemInfoType(TypedDict):
    rpi: str
    cpu: str
    total_mem: int
    dist: str


class SystemStatusType(TypedDict):
    using_mem: int
    num_proc: int
    temperature: List[float]
    current_time: str


class TermType(TypedDict):
    id: str
    created: str
    updated: str
