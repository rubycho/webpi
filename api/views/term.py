import atexit
import copy

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.urls import path

from api.utils.term import TerminalManager, TooMuchTerminal, ExitedTerminal
from .errors import missing_keys, wrong_keys, DataType


# TODO: lock method needed
manager = TerminalManager()


def cleanup():
    tmp = copy.copy(manager.term_pool)
    for term in tmp:
        manager.terminate(term.id)
    print("Successfully cleaned terminals")


class TerminalList(APIView):
    def get(self, request):
        return Response(manager.serialize())

    def post(self, request):
        try:
            return Response(manager.get(
                manager.create()
            ).serialize())
        except TooMuchTerminal:
            return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)


class TerminalDetail(APIView):
    def get(self, request, term_id: str):
        term = manager.get(term_id)
        if term is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(term.serialize())

    def put(self, request, term_id: str):
        term = manager.get(term_id)
        if term is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        req_type = request.data.get('type')
        if not req_type:
            return missing_keys(DataType.BODY, ['type'])

        if req_type == 'stdin':
            uinput = request.data.get('input')
            if uinput is None:
                return missing_keys(DataType.BODY, ['input'])
            try:
                term.stdin(uinput)
            except ExitedTerminal:
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response(status=status.HTTP_200_OK)
        elif req_type == 'stdout':
            return Response(term.stdout())
        else:
            return wrong_keys(DataType.BODY, ['type'])

    def delete(self, request, term_id: str):
        term = manager.get(term_id)
        if term is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        manager.terminate(term_id)
        return Response(status=status.HTTP_200_OK)


term_url_patterns = [
    path('term/', TerminalList.as_view()),
    path('term/<str:term_id>/', TerminalDetail.as_view())
]

atexit.register(cleanup)
