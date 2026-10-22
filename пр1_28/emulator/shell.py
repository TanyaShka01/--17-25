"""Цикл Read–Eval–Print Loop (REPL)."""
from .parser import parse_command
from .commands import execute


class Shell:
    def __init__(self, vfs_name="VFS", input_fn=input, output_fn=print):
        self.vfs_name = vfs_name
        self.input_fn = input_fn
        self.output_fn = output_fn

    @property
    def prompt(self):
        return f"{self.vfs_name}:/$ "

    def run(self):
        self.output_fn("Эмулятор UNIX-подобной оболочки. Введите help для справки.")
        while True:
            try:
                line = self.input_fn(self.prompt)
            except EOFError:
                self.output_fn("")
                break
            except KeyboardInterrupt:
                self.output_fn("")
                continue
            command = parse_command(line)
            if command is None:
                continue
            if not execute(command, self.output_fn):
                break
        self.output_fn("Работа эмулятора завершена.")
