import enum

from typing import List

from rest_framework import status
from rest_framework.response import Response


class DataType(enum.Enum):
    QUERY = 'query'
    PARAM = 'param'
    BODY = 'body'


def find_missing_keys(data: dict, keys: List[str]) -> (List[str], dict):
    missing = []
    marshaled = {}
    for key in keys:
        if key in data:
            marshaled[key] = data[key]
        else:
            missing.append(key)
    return missing, marshaled


def missing_keys(data_type: DataType, keys: List[str]) -> Response:
    errors = [
        'missing {} {}'.format(data_type.value, key) for key in keys
    ]
    return Response(
        data={'errors': errors},
        status=status.HTTP_400_BAD_REQUEST
    )


def wrong_keys(data_type: DataType, keys: List[str]) -> Response:
    errors = [
        'wrong {} {}'.format(data_type.value, key) for key in keys
    ]
    return Response(
        data={'errors': errors},
        status=status.HTTP_400_BAD_REQUEST
    )
