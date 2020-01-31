from django.shortcuts import render
from rest_framework.views import APIView


# System Information
class PiSpec(APIView):
    def get(self):
        pass


class FileManagerViewSet(APIView):
    def get(self):
        pass

    def post(self):
        pass

    def delete(self):
        pass


# GPIO Status, GPIO Macro, GPIO Trigger, PWM
class GPIOViewSet(APIView):
    def get(self):
        pass

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass


# camera, connected


# CPU Clock Set
class CPUClockViewSet(APIView):
    def get(self):
        pass

    def put(self):
        pass
