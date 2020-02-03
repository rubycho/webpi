from django.test import TestCase

from api.utils.proc import TopProcess


class ProcTest(TestCase):
    def test_get_process_list(self):
        TopProcess._get_process_list()

    def test_cpu_sorted(self):
        result = TopProcess.cpu_sorted()
        self.assertTrue(len(result) <= TopProcess.MAX_OUTPUT)

    def test_mem_sorted(self):
        result = TopProcess.mem_sorted()
        self.assertTrue(len(result) <= TopProcess.MAX_OUTPUT)
