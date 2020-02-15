from time import sleep
from django.test import TestCase

from api.utils.term import Terminal, TerminalManager, ExitedTerminal, TooMuchTerminal


class TerminalTest(TestCase):
    def setUp(self):
        self.term = Terminal()

    def test_alive(self):
        self.assertTrue(self.term.alive())

        self.term.cleanup()
        self.assertRaises(ExitedTerminal, self.term.alive_or_raise)

    def test_io(self):
        self.term.stdin('ls\n')

        sleep(0.1)
        self.assertTrue(
            len(self.term.stdout()) > 0
        )

    def test_serialize(self):
        self.term.serialize()

    def tearDown(self):
        self.term.cleanup()


class TerminalManagerTest(TestCase):
    def setUp(self):
        self.mg = TerminalManager()

    def test_create(self):
        for i in range(self.mg.TERM_MAX):
            self.mg.create()

        self.assertRaises(TooMuchTerminal, self.mg.create)

    def test_get(self):
        tid = self.mg.create()
        self.assertIsNotNone(self.mg.get(tid))

        tid = 'illegal'
        self.assertIsNone(self.mg.get(tid))

    def test_terminate(self):
        tid = self.mg.create()
        self.mg.terminate(tid)

        self.assertEqual(len(self.mg.term_pool), 0)

    def test_serialize(self):
        for i in range(self.mg.TERM_MAX):
            self.mg.create()
        result = self.mg.serialize()
        self.assertEqual(len(result), self.mg.TERM_MAX)

    def tearDown(self):
        for item in self.mg.term_pool:
            self.mg.terminate(item.id)
