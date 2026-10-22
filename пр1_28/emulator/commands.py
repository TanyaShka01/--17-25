"""Обработка команд. Файловые операции на первом этапе — заглушки."""
from .parser import Command

HELP = """Доступные команды:
  help  — справка
  exit  — выход
  ls    — список файлов (заглушка)
  cd    — смена каталога (заглушка)
  pwd   — текущий каталог (заглушка)
  cat   — чтение файла (заглушка)"""
STUB_COMMANDS = {"ls", "cd", "pwd", "cat"}


def execute(command: Command, output=print) -> bool:
    """Вернуть False для выхода, True для продолжения REPL."""
    name, arguments = command.name, command.arguments
    if name in {"help", "exit"}:
        if arguments:
            output(f"Использование: {name}")
            return True
        if name == "exit":
            return False
        output(HELP)
    elif name in STUB_COMMANDS:
        output(f"Команда: {name}")
        output(f"Аргументы: {arguments}")
        output("Функция пока не реализована (этап 1).")
    else:
        output(f"{name}: команда не найдена")
    return True
