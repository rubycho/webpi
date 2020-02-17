import enum

from typing import List

from rest_framework import status
from rest_framework.response import Response


class DataType(enum.Enum):
    """
    Constants, used on generating error strings.
    """
    QUERY = 'query'
    PARAM = 'param'
    BODY = 'body'


def extract_data(data: dict, keys: List[str]) -> (List[str], dict):
    """
    Extract data based on keys.

    :param data: dict-similar-typed source
    :param keys: keys to extract value from source
    :return: (keys that is not available on data, extracted data)
    """
    missing = []
    marshaled = {}
    for key in keys:
        if key in data:
            marshaled[key] = data[key]
        else:
            missing.append(key)
    return missing, marshaled


def missing_keys(data_type: DataType, keys: List[str]) -> Response:
    """
    Create BAD REQUEST Response.
    Indicate the request is missing query or param or body items.

    :param data_type: missing data type
    :param keys: missing item names
    :return: Response
    """
    errors = [
        'missing {} {}'.format(data_type.value, key) for key in keys
    ]
    return Response(
        data={'errors': errors},
        status=status.HTTP_400_BAD_REQUEST
    )


def wrong_keys(data_type: DataType, keys: List[str]) -> Response:
    """
    Create BAD REQUEST Response.
    Indicate the request has invalid query or param or body items.

    :param data_type: invalid data type
    :param keys: invalid item names
    :return: Response
    """
    errors = [
        'wrong {} {}'.format(data_type.value, key) for key in keys
    ]
    return Response(
        data={'errors': errors},
        status=status.HTTP_400_BAD_REQUEST
    )
