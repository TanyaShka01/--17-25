"""Чтение и проверка INI-конфигурации."""

import configparser
import os

REQUIRED_KEYS = (
    'package_name',
    'repo_url',
    'mode',
    'package_version',
    'output_format',
    'max_depth',
)
VALID_FORMATS = frozenset({'ascii_tree', 'plain', 'mermaid', 'svg'})
VALID_MODES = frozenset({'local', 'remote'})


def strip_value(section, key, default=''):
    """Возвращает значение параметра без пробелов по краям."""
    return str(section.get(key, default)).strip()


def is_empty(section, key):
    """Проверяет, что параметр отсутствует или пуст."""
    return not section.get(key) or not strip_value(section, key)


def find_missing(section):
    """Возвращает список обязательных параметров, которых нет."""
    return [key for key in REQUIRED_KEYS if is_empty(section, key)]


def check_choice(section, key, valid):
    """Проверяет, что значение входит в допустимый набор."""
    value = strip_value(section, key).lower()
    if value not in valid:
        allowed = ', '.join(sorted(valid))
        raise ValueError(f"{key} должен быть одним из: {allowed}")
    return value


def read_ini(section_name, path):
    """Читает раздел INI-файла и возвращает его."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"INI-файл не найден: {path}")
    parser = configparser.ConfigParser(interpolation=None)
    with open(path, 'r', encoding='utf-8') as handle:
        parser.read_file(handle)
    if not parser.has_section(section_name):
        raise KeyError(f"Раздел [{section_name}] не найден в INI.")
    return parser[section_name]


def parse_max_depth(raw):
    """Преобразует глубину графа в целое неотрицательное число."""
    try:
        value = int(raw)
    except ValueError as exc:
        raise ValueError("max_depth должен быть целым числом") from exc
    if value < 0:
        raise ValueError("max_depth не может быть отрицательным")
    return value


def load_config(path):
    """Читает и проверяет конфигурацию, возвращает словарь."""
    section = read_ini('settings', path)
    missing = find_missing(section)
    if missing:
        raise ValueError("Отсутствуют параметры: " + ", ".join(missing))
    return {
        'package_name': strip_value(section, 'package_name'),
        'repo_url': strip_value(section, 'repo_url'),
        'mode': check_choice(section, 'mode', VALID_MODES),
        'package_version': strip_value(section, 'package_version'),
        'output_format': check_choice(
            section, 'output_format', VALID_FORMATS),
        'max_depth': parse_max_depth(strip_value(section, 'max_depth')),
    }
