"""Построение графа зависимостей пакета."""


def get_dependencies(pkg_name):
    """Возвращает граф зависимостей пакета.

    Заглушка этапа 5: реальный парсер пакетных менеджеров появится
    позже, сейчас нужен только корректный словарь узлов и связей.
    """
    graphs = {
        'samplepkg': {
            'samplepkg': ['requests', 'pyyaml'],
            'requests': ['urllib3', 'certifi'],
            'pyyaml': [],
            'urllib3': [],
            'certifi': [],
        },
    }
    deps = graphs.get(
        pkg_name,
        {
            pkg_name: ['dependency_A', 'dependency_B'],
            'dependency_A': [],
            'dependency_B': [],
        },
    )
    return {'root': pkg_name, 'deps': deps}


def unvisited_children(graph, node, visited):
    """Возвращает дочерние узлы, которые ещё не обработаны."""
    children = graph['deps'].get(node, [])
    return [child for child in children if child not in visited]
