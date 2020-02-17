import os

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.urls import path
from django.http.response import FileResponse

from api.utils.disk import FileHandler
from .errors import DataType, extract_data, missing_keys, wrong_keys


@api_view(http_method_names=['GET'])
def download_file(request):
    """
    File Download API

    - Query
        - path: string, existing file's path

    - Response
        - 200: File
        - 400: Results if query is missing or invalid
    """
    missing, data = extract_data(request.GET, ['path'])
    if len(missing) > 0:
        return missing_keys(DataType.QUERY, missing)

    path = data.get('path')
    if not os.path.isfile(path):
        return wrong_keys(DataType.QUERY, ['path'])

    return FileResponse(open(path, 'rb'))


@api_view(http_method_names=['GET'])
def list_dir(request):
    """
    List Directory Contents API

    - Query
        - path: string, existing directory's path

    - Response
        - 200: [FileType,]
        - 400: Results if query is missing or invalid
    """
    missing, data = extract_data(request.GET, ['path'])
    if len(missing) > 0:
        return missing_keys(DataType.QUERY, missing)

    path = data.get('path')
    if not os.path.isdir(path):
        return wrong_keys(DataType.QUERY, ['path'])

    return Response(FileHandler.list(path))


@api_view(http_method_names=['POST'])
def upload_file(request):
    """
    File Upload API

    - Body
        - path: string, existing directory's path
        - file: File (multipart form-data)

    - Response
        - 200: Empty
        - 400: Results if body is incomplete or invalid
        - 500: Results if upload fails
    """
    missing, data = extract_data(request.data, ['path', 'file'])
    if len(missing) > 0:
        return missing_keys(DataType.BODY, missing)

    path = data.get('path')
    file = request.FILES.get('file')
    if not file:
        return wrong_keys(DataType.BODY, ['file'])

    if not os.path.isdir(path):
        return wrong_keys(DataType.BODY, ['path'])

    result = FileHandler.create_file(path, file)
    if not result:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(status=status.HTTP_200_OK)


@api_view(http_method_names=['POST'])
def create_dir(request):
    """
    Directory Creation API

    - Body
        - path: string, existing directory's path
        - dirname: string, valid directory name that doesn't include slashes

    - Response
        - 200: Empty
        - 400: Results if body is incomplete or invalid
        - 500: Results if creation fails
    """
    missing, data = extract_data(request.data, ['path', 'dirname'])
    if len(missing) > 0:
        return missing_keys(DataType.BODY, missing)

    path = data.get('path')
    dirname = data.get('dirname')
    if not os.path.isdir(path):
        return wrong_keys(DataType.BODY, ['path'])

    if dirname.find('/') >= 0 or \
        dirname.find('\\') >= 0:
        return wrong_keys(DataType.BODY, ['dirname'])

    result = FileHandler.create_dir(path, dirname)
    if not result:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(status=status.HTTP_200_OK)


@api_view(http_method_names=['POST'])
def delete_item(request):
    """
    File/Directory Deletion API

    - Body
        - path: string, existing file/directory's path

    -Response
        - 200: Empty
        - 400: Results if body is incomplete or invalid
        - 500: Results if deletion fails
    """
    missing, data = extract_data(request.data, ['path'])
    if len(missing) > 0:
        return missing_keys(DataType.BODY, missing)

    path = data.get('path')
    result = FileHandler.delete(path)
    if not result:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(status=status.HTTP_200_OK)


disk_url_patterns = [
    path('disk/download/', download_file, name='download-file'),
    path('disk/upload/', upload_file, name='upload-file'),
    path('disk/list/', list_dir, name='list-dir'),
    path('disk/create-dir/', create_dir, name='create-dir'),
    path('disk/delete/', delete_item, name='delete-item')
]
