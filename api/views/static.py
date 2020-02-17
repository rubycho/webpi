from django.urls import path
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.utils.system import SystemInfo, SystemStatus
from api.utils.proc import TopProcess


def index(request):
    return HttpResponse('Hello, world!')


@api_view(http_method_names=['GET'])
def pi_info(request):
    """
    Pi Info(Spec) API

    - Response
        - 200: SystemInfoType
    """
    return Response(SystemInfo.serialize())


@api_view(http_method_names=['GET'])
def pi_status(request):
    """
    Pi Status API

    - Response
        - 200: SystemStatusType
    """
    return Response(SystemStatus.serialize())


@api_view(http_method_names=['GET'])
def proc_cpu(request):
    """
    CPU-Sorted Top 10 Process List API

    - Response
        - 200: [ProcType,]
    """
    return Response(TopProcess.cpu_sorted())


@api_view(http_method_names=['GET'])
def proc_mem(request):
    """
    Memory-sorted Top 10 Process List API

    - Response
        - 200: [ProcType,]
    """
    return Response(TopProcess.mem_sorted())


static_url_patterns = [
    path('', index, name='index'),
    path('sys/pi-info/', pi_info, name='pi-status'),
    path('sys/pi-status/', pi_status, name='pi-status'),
    path('sys/proc-cpu/', proc_cpu, name='proc-cpu'),
    path('sys/proc-mem/', proc_mem, name='proc-mem')
]
