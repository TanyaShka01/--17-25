"""Форматы вывода графа: Mermaid, ASCII-дерево, plain."""

from depvis.graph import unvisited_children


def mermaid_edges(graph, max_depth):
    """Собирает уникальные связи графа в виде строк Mermaid."""
    visited = {graph['root']}
    edges = []
    frontier = [(graph['root'], 0)]
    while frontier:
        node, depth = frontier.pop(0)
        if depth > max_depth:
            continue
        for child in unvisited_children(graph, node, visited):
            edge = f"    {node} --> {child}"
            if edge not in edges:
                edges.append(edge)
            visited.add(child)
            frontier.append((child, depth + 1))
    return edges


def generate_mermaid(graph, max_depth):
    """Генерирует Mermaid-код для графа зависимостей."""
    lines = ['graph TD'] + mermaid_edges(graph, max_depth)
    return '\n'.join(lines)


def render_ascii_tree(graph, max_depth):
    """Рисует дерево зависимостей псевдографикой."""
    lines = [graph['root']]
    seen = {graph['root']}
    stack = [(graph['root'], 0, '')]
    while stack:
        node, depth, prefix = stack.pop()
        if depth >= max_depth + 1:
            continue
        children = unvisited_children(graph, node, seen)
        for index, child in enumerate(children):
            seen.add(child)
            last = index == len(children) - 1
            lines.append(prefix + ('└─ ' if last else '├─ ') + child)
            step = '   ' if last else '│  '
            stack.append((child, depth + 1, prefix + step))
    return '\n'.join(lines)


def render_plain(graph):
    """Выводит пары «пакет -> зависимость» обычным текстом."""
    lines = []
    for node in sorted(graph['deps']):
        for child in graph['deps'][node]:
            lines.append(f"{node} -> {child}")
    return '\n'.join(lines) if lines else '(зависимостей нет)'


def render_graph(graph, cfg):
    """Возвращает текст графа для выбранного формата вывода."""
    fmt = cfg['output_format']
    if fmt == 'ascii_tree':
        return render_ascii_tree(graph, cfg['max_depth'])
    if fmt == 'plain':
        return render_plain(graph)
    return generate_mermaid(graph, cfg['max_depth'])
