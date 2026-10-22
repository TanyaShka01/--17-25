import unittest
from emulator.parser import parse_command, Command
from emulator.commands import execute
from emulator.shell import Shell


class ParserTests(unittest.TestCase):
    def test_split(self):
        self.assertEqual(parse_command("  ls   -l /home  "), Command("ls", ["-l", "/home"]))

    def test_empty(self):
        self.assertIsNone(parse_command("  "))

    def test_quotes_are_literal(self):
        self.assertEqual(parse_command('cat "a b"').arguments, ['"a', 'b"'])


class CommandTests(unittest.TestCase):
    def test_stub(self):
        out = []
        self.assertTrue(execute(Command("ls", ["-l"]), out.append))
        self.assertIn("Аргументы: ['-l']", out)

    def test_unknown(self):
        out = []
        self.assertTrue(execute(Command("unknown", []), out.append))
        self.assertEqual(out, ["unknown: команда не найдена"])

    def test_exit(self):
        self.assertFalse(execute(Command("exit", []), lambda _: None))
        self.assertTrue(execute(Command("exit", ["extra"]), lambda _: None))

    def test_help(self):
        out = []
        self.assertTrue(execute(Command("help", []), out.append))
        self.assertIn("Доступные команды:", out[0])


class ShellTests(unittest.TestCase):
    def run_script(self, events):
        events = iter(events)
        out, prompts = [], []

        def read(prompt):
            prompts.append(prompt)
            event = next(events)
            if isinstance(event, BaseException):
                raise event
            return event

        Shell("TestVFS", read, out.append).run()
        return out, prompts

    def test_repl(self):
        out, prompts = self.run_script(["", "ls /home", "exit"])
        self.assertEqual(prompts, ["TestVFS:/$ "] * 3)
        self.assertIn("Аргументы: ['/home']", out)

    def test_eof(self):
        out, prompts = self.run_script([EOFError()])
        self.assertEqual(len(prompts), 1)
        self.assertEqual(out[-1], "Работа эмулятора завершена.")

    def test_interrupt(self):
        _, prompts = self.run_script([KeyboardInterrupt(), "exit"])
        self.assertEqual(len(prompts), 2)


if __name__ == "__main__":
    unittest.main()
