from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.http.response import FileResponse

from api.utils.disk import FileHandler
from .errors import DataType, find_missing_keys, missing_keys, wrong_keys


@api_view(http_method_names=['GET'])
def download_file(request):
    missing, data = find_missing_keys(request.GET, ['path'])
    if len(missing) > 0:
        return missing_keys(DataType.QUERY, missing)

    path = data.get('path')
    if (not FileHandler.exists(path)) or \
            FileHandler.is_dir(path):
        return wrong_keys(DataType.QUERY, ['path'])

    return FileResponse(open(path, 'rb'))


@api_view(http_method_names=['GET'])
def list_dir(request):
    missing, data = find_missing_keys(request.GET, ['path'])
    if len(missing) > 0:
        return missing_keys(DataType.QUERY, missing)

    path = data.get('path')
    if (not FileHandler.exists(path)) or \
            (not FileHandler.is_dir(path)):
        return wrong_keys(DataType.QUERY, ['path'])

    return Response(FileHandler.list(path))


@api_view(http_method_names=['POST'])
def upload_file(request):
    missing, data = find_missing_keys(request.data, ['path', 'file'])
    if len(missing) > 0:
        return missing_keys(DataType.BODY, missing)

    path = data.get('path')
    file = request.FILES.get('file')
    if not file:
        return wrong_keys(DataType.BODY, ['file'])

    if (not FileHandler.exists(path)) or \
            (not FileHandler.is_dir(path)):
        return wrong_keys(DataType.BODY, ['path'])

    result = FileHandler.create_file(path, file)
    if not result:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(status=status.HTTP_200_OK)


@api_view(http_method_names=['POST'])
def create_dir(request):
    missing, data = find_missing_keys(request.data, ['path', 'dirname'])
    if len(missing) > 0:
        return missing_keys(DataType.BODY, missing)

    path = data.get('path')
    dirname = data.get('dirname')
    if (not FileHandler.exists(path)) or \
            (not FileHandler.is_dir(path)):
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
    missing, data = find_missing_keys(request.data, ['path'])
    if len(missing) > 0:
        return missing_keys(DataType.BODY, missing)

    path = data.get('path')
    result = FileHandler.delete(path)
    if not result:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(status=status.HTTP_200_OK)
