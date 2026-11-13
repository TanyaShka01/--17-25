"""Запуск внешних команд и генерация SVG через
mmdc."""

import os
import shlex
import subprocess

try:
    import matplotlib.pyplot as plt
    import networkx as nx
    HAS_PLOTTING = True
except ImportError:
    HAS_PLOTTING = False

PPTR_ARGS = (
    '{"args": ["--no-sandbox", "--disable-setuid-sandbox"]}'
)


def write_text(path, text):
    """Сохраняет текст в файл в кодировке
    UTF-8."""
    with open(path, 'w', encoding='utf-8') as handle:
        handle.write(text)


def create_puppeteer_config(out_dir):
    """Создаёт конфиг Puppeteer для запуска без
    песочницы."""
    path = os.path.join(out_dir, 'puppeteer-config.json')
    write_text(path, PPTR_ARGS)
    return path


def build_mmdc_command(mmd_path, svg_path, pptr_path):
    """Собирает список аргументов для mmdc без
    ручных кавычек."""
    return [
        'mmdc', '-i', mmd_path, '-o', svg_path, '-p', pptr_path
    ]


def to_command_line(args):
    """Преобразует список аргументов в строку с
    экранированием."""
    if os.name == 'nt':
        return subprocess.list2cmdline(args)
    return ' '.join(shlex.quote(arg) for arg in args)


def run_command(args, cwd=None):
    """Запускает команду и возвращает результат
    subprocess."""
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
    """Генерирует SVG из Mermaid-файла через
    mmdc."""
    svg_path = os.path.join(out_dir, f"{pkg_name}_deps.svg")
    pptr_path = create_puppeteer_config(out_dir)
    args = build_mmdc_command(mmd_path, svg_path, pptr_path)
    try:
        result = run_command(args)
    except OSError as exc:
        print(f"Системная ошибка: {exc}")
        return None
    if result.returncode != 0:
        print(
            f"Ошибка при генерации SVG:\n"
            f"{result.stderr.strip()}"
        )
        return None
    print(f"SVG успешно сохранён: {svg_path}")
    return svg_path


def create_graph_image(graph, out_dir, pkg_name):
    """Создаёт изображение графа с помощью
    matplotlib и networkx."""
    if not HAS_PLOTTING:
        print("Для создания изображения установите "
              "библиотеки:")
        print("  pip install matplotlib networkx")
        return None

    G = nx.DiGraph()

    for node, deps in graph['deps'].items():
        G.add_node(node)
        for dep in deps:
            G.add_edge(node, dep)

    if len(G.nodes) == 0:
        G.add_node(graph['root'])

    plt.figure(figsize=(12, 8))

    try:
        pos = nx.spring_layout(
            G, k=2, iterations=50, seed=42
        )
    except:
        pos = nx.shell_layout(G)

    nx.draw_networkx_nodes(
        G, pos, node_color='lightblue',
        node_size=3000, alpha=0.9
    )
    nx.draw_networkx_labels(
        G, pos, font_size=10, font_weight='bold'
    )
    nx.draw_networkx_edges(
        G, pos, edge_color='gray', arrows=True,
        arrowsize=20, arrowstyle='->', width=2
    )

    plt.title(
        f"Граф зависимостей: {pkg_name}",
        fontsize=16, fontweight='bold'
    )
    plt.axis('off')
    plt.tight_layout()

    png_path = os.path.join(out_dir, f"{pkg_name}_deps.png")
    try:
        plt.savefig(
            png_path, dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none'
        )
        plt.close()
        print(
            f"PNG изображение успешно сохранено: "
            f"{png_path}"
        )
        return png_path
    except Exception as exc:
        print(
            f"Ошибка при сохранении изображения: {exc}"
        )
        plt.close()
        return None


def export_mermaid(out_dir, pkg_name, code, fmt, graph=None):
    """Сохраняет .mmd и при необходимости
    генерирует .svg или .png."""
    mmd_path = os.path.join(out_dir, f"{pkg_name}_deps.mmd")
    write_text(mmd_path, code + '\n')
    print(f"Mermaid-файл сохранён: {mmd_path}")

    if graph is not None:
        create_graph_image(graph, out_dir, pkg_name)

    if fmt == 'svg':
        svg_result = export_svg(mmd_path, out_dir, pkg_name)
        if svg_result is None:
            print(
                "Примечание: SVG не создан через mmdc, "
                "но PNG изображение доступно"
            )

    return mmd_path
