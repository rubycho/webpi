import os
from pathlib import Path

from django.test import TestCase
from unittest import mock

from api.utils.disk import FileHandler


class DiskTest(TestCase):
    TEST_PATH = '/tmp/'

    def test_list(self):
        file_cnt = len(os.listdir(self.TEST_PATH))
        result = FileHandler.list(self.TEST_PATH)
        self.assertEqual(file_cnt, len(result))

    def test_exists(self):
        test_file = str(os.path.join(self.TEST_PATH, 'test_exists.txt'))

        Path(test_file).touch()
        self.assertTrue(FileHandler.exists(test_file))
        Path(test_file).unlink()
        self.assertFalse(FileHandler.exists(test_file))

    def test_create_file(self):
        test_file_name = 'test_create_file.txt'
        test_file = str(os.path.join(self.TEST_PATH, test_file_name))

        file = mock.Mock()
        file.name = test_file_name
        file.chunks.return_value = [b'a', b'b', b'c', b'd']

        self.assertTrue(FileHandler.create_file(self.TEST_PATH, file))
        self.assertTrue(os.path.exists(test_file))

        file.name += '/\\illegal'
        self.assertFalse(FileHandler.create_file(self.TEST_PATH, file))

        os.unlink(test_file)

    def test_create_dir(self):
        test_dirname = 'test_dir'
        test_dir = str(os.path.join(self.TEST_PATH, test_dirname))

        self.assertTrue(FileHandler.create_dir(self.TEST_PATH, test_dirname))
        self.assertTrue(os.path.exists(test_dir))
        os.rmdir(test_dir)

        test_dirname += '/' + test_dirname
        self.assertFalse(FileHandler.create_dir(self.TEST_PATH, test_dirname))

    def test_delete(self):
        test_file_name = 'test_delete.txt'
        test_dirname = 'test_delete'
        test_file = str(os.path.join(self.TEST_PATH, test_file_name))
        test_dir = str(os.path.join(self.TEST_PATH, test_dirname))

        Path(test_file).touch()
        self.assertTrue(FileHandler.delete(test_file))
        self.assertFalse(os.path.exists(test_file))

        self.assertFalse(FileHandler.delete(test_file))

        os.mkdir(test_dir)
        self.assertTrue(FileHandler.delete(test_dir))
        self.assertFalse(os.path.exists(test_dir))

        self.assertFalse(FileHandler.delete(test_file))
