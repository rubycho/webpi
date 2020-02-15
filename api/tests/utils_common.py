from django.test import TestCase


from api.utils.common import find_line, find_value


class CommonTest(TestCase):
    def test_find_line(self):
        lines = [
            'Hello, Test string',
            'world, Test string'
        ]

        self.assertEqual(
            find_line(lines, 'Hello,'),
            lines[0]
        )
        self.assertEqual(
            find_line(lines, 'world,'),
            lines[1]
        )

        self.assertEqual(
            find_line(lines, 'Foo,'),
            ''
        )
        self.assertEqual(
            find_line(lines, 'Foo,', 'Bar'),
            'Bar'
        )

    def test_find_value(self):
        lines = [
            'VALUE=Hello',
            'VALUE:world'
        ]
        value = ['Hello', 'world']

        self.assertEqual(
            find_value(lines[0], '='),
            value[0]
        )
        self.assertEqual(
            find_value(lines[1], ':'),
            value[1]
        )
