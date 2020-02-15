from django.urls import path

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response

from .errors import find_missing_keys, missing_keys, wrong_keys, DataType
from api.utils.gpio import GPIOGetter, GPIOSetter, PinNotAllowed


@api_view(http_method_names=['GET'])
def gpio_list(request):
    return Response(GPIOGetter.list())


class GPIODetail(APIView):
    def get(self, request, pin: int):
        try:
            return Response(GPIOGetter.get(pin))
        except PinNotAllowed:
            return wrong_keys(DataType.PARAM, ['pin'])

    def put(self, request, pin: int):
        try:
            GPIOGetter.get(pin)
        except PinNotAllowed:
            return wrong_keys(DataType.PARAM, ['pin'])

        req_type = request.data.get('type')
        if not req_type:
            return missing_keys(DataType.BODY, ['type'])

        if req_type == 'mode':
            mode = request.data.get(req_type)
            if mode is None:
                return missing_keys(DataType.BODY, [req_type])

            GPIOSetter.mode(pin, int(mode))
        elif req_type == 'value':
            value = request.data.get(req_type)
            if value is None:
                return missing_keys(DataType.BODY, [req_type])

            GPIOSetter.value(pin, int(value))
        elif req_type == 'pwm':
            missing, data = find_missing_keys(request.data, ['dutycycle', 'freq'])
            if len(missing) > 0:
                return missing_keys(DataType.BODY, missing)

            GPIOSetter.pwm_dutycycle(pin, int(data.get('dutycycle')))
            GPIOSetter.pwm_freq(pin, int(data.get('freq')))
        else:
            return wrong_keys(DataType.BODY, ['type'])

        return Response(status=status.HTTP_200_OK)


gpio_url_patterns = [
    path('gpio/', gpio_list, name='gpio-list'),
    path('gpio/<int:pin>/', GPIODetail.as_view())
]
