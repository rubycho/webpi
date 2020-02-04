import os
import time
import shutil
import pathlib
from typing import List

from django.core.files.uploadedfile import UploadedFile
from api.utils.types import FileType


class FileHandler:
    @classmethod
    def list(cls, path: str) -> List[FileType]:
        file_list = []
        for file in pathlib.Path(path).iterdir():
            file_list.append(
                {
                    'name': file.name,
                    'is_dir': file.is_dir(),
                    'created': time.ctime(file.stat().st_ctime),
                    'modified': time.ctime(file.stat().st_mtime),
                    'size': file.stat().st_size
                }
            )
        return file_list

    @classmethod
    def exists(cls, path: str) -> bool:
        return os.path.exists(path)

    @classmethod
    def is_dir(cls, path: str) -> bool:
        return os.path.isdir(path)

    @classmethod
    def create_file(cls, path: str, file: UploadedFile) -> bool:
        try:
            with open(os.path.join(path, file.name), 'wb') as f:
                for chunk in file.chunks():
                    f.write(chunk)
            return True
        except OSError:
            return False

    @classmethod
    def create_dir(cls, path: str, dirname: str) -> bool:
        try:
            os.mkdir(os.path.join(path, dirname))
            return True
        except OSError:
            return False

    @classmethod
    def delete(cls, path: str) -> bool:
        try:
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.unlink(path)
            return True
        except OSError:
            return False
