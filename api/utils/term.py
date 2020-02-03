import os
import time
from typing import List
from datetime import datetime
from subprocess import Popen, PIPE

from .types import TermType


class Terminal:
    def __init__(self):
        self.id = str(time.time())
        self.created = datetime.now()
        self.updated = datetime.now()

        self.fw = open('/tmp/{}'.format(self.id), 'wb')
        self.fr = open('/tmp/{}'.format(self.id), 'r')
        self.process = Popen('bash',
                             stdin=PIPE,
                             stdout=self.fw,
                             stderr=self.fw,
                             env=os.environ.copy(),
                             bufsize=1)

    def alive(self) -> bool:
        return self.process.poll() is None

    def alive_or_raise(self):
        if not self.alive():
            raise ExitedTerminal(self.id)

    def stdin(self, uinput: str):
        self.alive_or_raise()
        self.process.stdin.write(bytes(uinput.encode('utf-8')))
        self.process.stdin.flush()
        self.updated = datetime.now()

    def stdout(self) -> str:
        self.alive_or_raise()
        return self.fr.read()

    def cleanup(self):
        self.fr.close()
        self.fw.close()
        if self.alive():
            self.process.kill()
        try:
            os.remove('/tmp/{}'.format(self.id))
        except OSError:
            pass

    def serialize(self) -> TermType:
        return {
            'id': self.id,
            'created': self.created.strftime('%c'),
            'updated': self.updated.strftime('%c')
        }


class TerminalManager:
    TERM_MAX = 5

    def __init__(self):
        self.term_pool: List[Terminal] = []

    def create(self) -> str:
        if len(self.term_pool) >= self.TERM_MAX:
            raise TooMuchTerminal(self.TERM_MAX)

        new_term = Terminal()
        self.term_pool.append(new_term)
        return new_term.id

    def get(self, term_id: str) -> Terminal or None:
        for term in self.term_pool:
            if term.id == term_id:
                return term
        return None

    def terminate(self, term_id: str):
        term = self.get(term_id)
        if term is not None:
            term.cleanup()
            self.term_pool.remove(term)

    def serialize(self) -> List[TermType]:
        return [term.serialize() for term in self.term_pool]


class TooMuchTerminal(Exception):
    def __init__(self, term_max: int):
        super().__init__('maximum terminals reached: max={}'.format(term_max))


class ExitedTerminal(Exception):
    def __init__(self, term_id: str):
        super().__init__('terminal already exited: id={}'.format(term_id))
