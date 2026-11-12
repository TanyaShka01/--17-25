"""Командный интерфейс утилиты depvis."""

import argparse
import os
import sys

from depvis.config import load_config
from depvis.exporters import export_mermaid
from depvis.gitrepo import commit_output, prepare_output_dir, save_summary
from depvis.graph import get_dependencies
from depvis.render import render_graph

TITLE = 'Этап 5: Визуализация графа зависимостей'


def print_params(cfg):
    """Печатает параметры конфигурации в отсортированном виде."""
    for key in sorted(cfg.keys()):
        print(f"{key} = {cfg[key]}")


def build_parser():
    """Создаёт парсер аргументов командной строки."""
    parser = argparse.ArgumentParser(description=TITLE)
    parser.add_argument(
        '--config',
        default='config.ini',
        help='Путь к INI-файлу',
    )
    return parser


def run(args):
    """Основной сценарий: конфиг, граф, отчёт и коммит."""
    try:
        cfg = load_config(args.config)
    except (OSError, KeyError, ValueError) as exc:
        print(f"Ошибка: {exc}")
        return 1
    print("Параметры конфигурации:")
    print_params(cfg)
    cwd = os.getcwd()
    out_dir = prepare_output_dir()
    graph = get_dependencies(cfg['package_name'])
    body = render_graph(graph, cfg)
    save_summary(out_dir, cfg, graph, body)
    export_mermaid(out_dir, cfg['package_name'], body, cfg['output_format'])
    commit_output(cwd, out_dir)
    return 0


def main(argv=None):
    """Точка входа скрипта."""
    args = build_parser().parse_args(argv)
    return run(args)


if __name__ == '__main__':
    sys.exit(main())
