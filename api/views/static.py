from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.utils.system import SystemInfo, SystemStatus
from api.utils.proc import TopProcess


def index(request):
    return HttpResponse('Hello, world!')


@api_view(http_method_names=['GET'])
def pi_info(request):
    return Response(SystemInfo.serialize())


@api_view(http_method_names=['GET'])
def pi_status(request):
    return Response(SystemStatus.serialize())


@api_view(http_method_names=['GET'])
def proc_cpu(request):
    return Response(TopProcess.cpu_sorted())


@api_view(http_method_names=['GET'])
def proc_mem(request):
    return Response(TopProcess.mem_sorted())
