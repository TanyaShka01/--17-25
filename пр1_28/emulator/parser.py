"""Простой разбор команды по пробельным символам."""
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Command:
    name: str
    arguments: List[str]


def parse_command(line: str) -> Optional[Command]:
    """Первое слово — команда, остальные слова — аргументы.

    Кавычки, экранирование, конвейеры и переменные не интерпретируются.
    """
    parts = line.split()
    if not parts:
        return None
    return Command(parts[0], parts[1:])
