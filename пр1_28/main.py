"""Точка входа консольного эмулятора."""
import argparse
from emulator.shell import Shell


def main():
    parser = argparse.ArgumentParser(description="Вариант 28: эмулятор оболочки, этап 1")
    parser.add_argument("--vfs-name", default="VFS", help="имя VFS в приглашении")
    args = parser.parse_args()
    if not args.vfs_name.strip() or not args.vfs_name.isprintable():
        parser.error("имя VFS должно быть непустым и содержать печатные символы")
    Shell(args.vfs_name).run()


if __name__ == "__main__":
    main()
