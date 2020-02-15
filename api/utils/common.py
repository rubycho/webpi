from typing import List


def find_line(lines: List[str],
              keyword: str,
              fallback: str = '') -> str:
    for line in lines:
        if line.startswith(keyword):
            return line.replace('\n', '')
    return fallback


def find_value(line: str,
               delimiter: str) -> str:
    return line.split(delimiter)[-1]
