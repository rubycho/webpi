import atexit
import copy

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.urls import path

from api.utils.term import TerminalManager, TooMuchTerminal, ExitedTerminal
from .errors import extract_data, missing_keys, wrong_keys, DataType


# TODO: lock method needed
manager = TerminalManager()


def cleanup():
    """
    Cleans up existing terminals before exit.
    """
    tmp = copy.copy(manager.term_pool)
    for term in tmp:
        manager.terminate(term.id)


class TerminalList(APIView):
    def get(self, request):
        """
        Terminal Status List API

        - Response
            - 200: [TermType,]
        """
        return Response(manager.serialize())

    def post(self, request):
        """
        Terminal Creation API

        - Response
            - 200: TermType, with password
            - 503: Results if TerminalManager.TERM_MAX terminals are running
        """
        try:
            term = manager.get(manager.create())
            data = term.serialize()
            data['password'] = term.password
            return Response(data)
        except TooMuchTerminal:
            return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)


class TerminalDetail(APIView):
    def get(self, request, term_id: str):
        """
        Terminal Status API

        - Param
            - term_id: string, Terminal's id

        - Response
            - 200: TermType
            - 404: Results if there is no such terminal with provided id
        """
        term = manager.get(term_id)
        if term is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(term.serialize())

    def put(self, request, term_id: str):
        """
        Terminal Communication API

        - Param
            - term_id: string, Terminal's id

        - Body Type 1
            - type: 'stdin'
            - password: string, password which is provided on creation
            - input: string, command to execute

        - Response for Type 1
            - 200: Empty
            - 500: Results if terminal's subprocess (bash) has exited

        - Body Type 2
            - type: 'stdout'
            - password: string, password which is provided on creation

        - Response for Type 2
            - 200: string, stdout

        - Response
            - 400: Results if body is incomplete or invalid
            - 404: Results if there is no such terminal with provided id
        """
        term = manager.get(term_id)
        if term is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        missing, data = extract_data(request.data, ['type', 'password'])
        if len(missing) > 0:
            return missing_keys(DataType.BODY, missing)

        # password check
        if term.password != data.get('password'):
            return wrong_keys(DataType.BODY, ['password'])

        req_type = data.get('type')
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
        """
        Terminal Termination API

        - Param
            - term_id: string, Terminal's id

        - Respnose
            - 200: Empty
            - 404: Results if there is no such terminal with provided id
        """
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
