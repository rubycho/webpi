from django.test import TestCase

from api.utils.system import SystemInfo, SystemStatus


class SystemTest(TestCase):
    def test_system_info(self):
        SystemInfo.serialize()

    def test_system_status(self):
        SystemStatus.serialize()
