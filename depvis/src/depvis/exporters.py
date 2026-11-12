"""Запуск внешних команд и генерация SVG через mmdc."""

import os
import shlex
import subprocess

PPTR_ARGS = '{"args": ["--no-sandbox", "--disable-setuid-sandbox"]}'


def write_text(path, text):
    """Сохраняет текст в файл в кодировке UTF-8."""
    with open(path, 'w', encoding='utf-8') as handle:
        handle.write(text)


def create_puppeteer_config(out_dir):
    """Создаёт конфиг Puppeteer для запуска без песочницы."""
    path = os.path.join(out_dir, 'puppeteer-config.json')
    write_text(path, PPTR_ARGS)
    return path


def build_mmdc_command(mmd_path, svg_path, pptr_path):
    """Собирает список аргументов для mmdc без ручных кавычек."""
    return ['mmdc', '-i', mmd_path, '-o', svg_path, '-p', pptr_path]


def to_command_line(args):
    """Преобразует список аргументов в строку с экранированием."""
    if os.name == 'nt':
        return subprocess.list2cmdline(args)
    return ' '.join(shlex.quote(arg) for arg in args)


def run_command(args, cwd=None):
    """Запускает команду и возвращает результат subprocess."""
    return subprocess.run(
        to_command_line(args),
        shell=True,
        cwd=cwd,
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='replace',
    )


def export_svg(mmd_path, out_dir, pkg_name):
    """Генерирует SVG из Mermaid-файла через mmdc."""
    svg_path = os.path.join(out_dir, f"{pkg_name}_deps.svg")
    pptr_path = create_puppeteer_config(out_dir)
    args = build_mmdc_command(mmd_path, svg_path, pptr_path)
    try:
        result = run_command(args)
    except OSError as exc:
        print(f"Системная ошибка: {exc}")
        return None
    if result.returncode != 0:
        print(f"Ошибка при генерации SVG:\n{result.stderr.strip()}")
        return None
    print(f"SVG успешно сохранён: {svg_path}")
    return svg_path


def export_mermaid(out_dir, pkg_name, code, fmt):
    """Сохраняет .mmd и при необходимости генерирует .svg."""
    mmd_path = os.path.join(out_dir, f"{pkg_name}_deps.mmd")
    write_text(mmd_path, code + '\n')
    print(f"Mermaid-файл сохранён: {mmd_path}")
    if fmt == 'svg':
        export_svg(mmd_path, out_dir, pkg_name)
    return mmd_path
