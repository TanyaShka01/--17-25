"""Сохранение сводного отчёта и работа с Git-репозиторием."""

import os

from depvis.exporters import run_command, write_text

TITLE = 'Этап 5: Визуализация графа зависимостей'
COMMIT_MSG = 'feat(depvis): визуализация графа зависимостей'
OUTPUT_DIR = 'ep5_output'


def prepare_output_dir():
    """Создаёт выходную папку и возвращает её путь."""
    out_dir = os.path.join(os.getcwd(), OUTPUT_DIR)
    os.makedirs(out_dir, exist_ok=True)
    return out_dir


def save_summary(out_dir, cfg, graph, body):
    """Пишет сводный отчёт по результатам работы."""
    lines = [TITLE, '']
    for key in sorted(cfg.keys()):
        lines.append(f"{key} = {cfg[key]}")
    lines.extend(['', f"Узлов в графе: {len(graph['deps'])}", '', body, ''])
    path = os.path.join(out_dir, 'ep5_summary.txt')
    write_text(path, '\n'.join(lines))
    return path


def git_add(cwd, target):
    """Индексирует файлы выходной папки."""
    return run_command(['git', 'add', '--', target], cwd=cwd)


def git_commit(cwd, message):
    """Создаёт коммит с заданным сообщением."""
    return run_command(['git', 'commit', '-m', message], cwd=cwd)


def git_status(cwd):
    """Возвращает вывод git status --porcelain."""
    return run_command(['git', 'status', '--porcelain'], cwd=cwd).stdout


def ensure_git(cwd):
    """Инициализирует локальный репозиторий при необходимости."""
    if os.path.exists(os.path.join(cwd, '.git')):
        return
    run_command(['git', 'init'], cwd=cwd)
    run_command(['git', 'config', 'user.email', 'bot@example.com'], cwd=cwd)
    run_command(['git', 'config', 'user.name', 'SYNTX Bot'], cwd=cwd)


def commit_output(cwd, out_dir):
    """Коммитит изменения выходной папки, если они есть."""
    ensure_git(cwd)
    git_add(cwd, os.path.relpath(out_dir, cwd))
    if git_status(cwd).strip():
        git_commit(cwd, COMMIT_MSG)
        print("Изменения закоммичены в Git.")
        return True
    print("Нет изменений для коммита.")
    return False
