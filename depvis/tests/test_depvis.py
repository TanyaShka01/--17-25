"""Тесты конфигурации, графа и рендеринга."""

import os

import pytest

from depvis.config import load_config, parse_max_depth
from depvis.graph import get_dependencies
from depvis.render import generate_mermaid, render_plain

CONFIG_BODY = """[settings]
package_name = samplepkg
repo_url = /path/to/test_repo
mode = local
package_version = 1.0.0
output_format = mermaid
max_depth = 2
"""


@pytest.fixture
def config_file(tmp_path):
    """Создаёт временный INI-файл с корректными
    параметрами."""
    path = tmp_path / 'config.ini'
    path.write_text(CONFIG_BODY, encoding='utf-8')
    return str(path)


def test_load_config_ok(config_file):
    """Корректный файл читается без ошибок."""
    cfg = load_config(config_file)
    assert cfg['package_name'] == 'samplepkg'
    assert cfg['max_depth'] == 2


def test_load_config_missing_file():
    """Отсутствующий файл даёт
    FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        load_config(
            os.path.join('no', 'such', 'config.ini')
        )


def test_load_config_empty_value(tmp_path):
    """Пустое значение попадает в список
    отсутствующих."""
    path = tmp_path / 'bad.ini'
    body = CONFIG_BODY.replace(
        'package_name = samplepkg',
        'package_name ='
    )
    path.write_text(body, encoding='utf-8')
    with pytest.raises(ValueError):
        load_config(str(path))


def test_parse_max_depth_negative():
    """Отрицательная глубина запрещена."""
    with pytest.raises(ValueError):
        parse_max_depth('-1')


def test_mermaid_contains_edges():
    """Mermaid-код содержит корень и связи."""
    graph = get_dependencies('samplepkg')
    code = generate_mermaid(graph, 2)
    assert code.startswith('graph TD')
    assert 'samplepkg --> requests' in code


def test_mermaid_respects_depth():
    """Связи глубже лимита не попадают в граф."""
    graph = get_dependencies('samplepkg')
    code = generate_mermaid(graph, 0)
    assert 'urllib3 --> ' not in code


def test_plain_output():
    """Plain-формат перечисляет пары узлов."""
    graph = get_dependencies('samplepkg')
    assert 'requests -> urllib3' in render_plain(graph)
