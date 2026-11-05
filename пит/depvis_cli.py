import argparse, configparser, os, sys
import subprocess


def load_config(path):
    cp = configparser.ConfigParser(interpolation=None)
    if not os.path.exists(path):
        raise FileNotFoundError(f"INI-файл не найден: {path}")
    with open(path, 'r', encoding='utf-8') as f:
        cp.read_file(f)
    if 'settings' not in cp:
        raise KeyError("Раздел [settings] не найден в INI.")
    s = cp['settings']
    required = ['package_name','repo_url','mode','package_version','output_format','max_depth']
    missing = [k for k in required if k not in s or str(s[k]).strip() == ""]
    if missing:
        raise ValueError("Отсутствуют параметры: " + ", ".join(missing))
    
    # Добавим новые форматы вывода: mermaid и svg
    valid_formats = {'ascii_tree', 'plain', 'mermaid', 'svg'}
    if s['output_format'].strip().lower() not in valid_formats:
        raise ValueError(f"output_format должен быть одним из: {valid_formats}")

    cfg = {
        'package_name': s['package_name'].strip(),
        'repo_url': s['repo_url'].strip(),
        'mode': s['mode'].strip().lower(),
        'package_version': s['package_version'].strip(),
        'output_format': s['output_format'].strip().lower(),
        'max_depth': int(s['max_depth'])
    }
    return cfg

def get_dependencies(pkg_name):
    """
    ЗАГЛУШКА: Здесь должен быть реальный парсер зависимостей.
    Для этапа 5 мы формируем словарь графа (узлы и связи).
    """
    # Пример графа для демонстрации
    if pkg_name == 'samplepkg':
        return {
            'root': 'samplepkg',
            'deps': {
                'samplepkg': ['requests', 'pyyaml'],
                'requests': ['urllib3', 'certifi'],
                'pyyaml': [],
                'urllib3': [],
                'certifi': []
            }
        }
    else:
        # Простой дефолтный граф для любого другого пакета
        return {
            'root': pkg_name,
            'deps': {pkg_name: ['dependency_A', 'dependency_B'], 'dependency_A': [], 'dependency_B': []}
        }

def generate_mermaid(graph, max_depth, current_depth=0, visited=None):
    """Рекурсивно генерирует Mermaid-код для графа зависимостей."""
    if visited is None:
        visited = set()
    
    root = graph['root']
    lines = ["graph TD"]
    
    def walk(node, depth):
        if depth > max_depth or node not in graph['deps']:
            return
        for child in graph['deps'][node]:
            lines.append(f"    {node} --> {child}")
            if child not in visited:
                visited.add(child)
                walk(child, depth + 1)

    visited.add(root)
    walk(root, 0)
    
    # Убираем дубликаты строк (если граф сложный)
    unique_lines = list(dict.fromkeys(lines))
    return "\n".join(unique_lines)

def render_ascii_tree(pkg, depth_limit, depth=1):
    # Оставляем для совместимости со старым форматом
    lines = [pkg]
    if depth_limit <= 0: return "\n".join(lines)
    if depth_limit >= 1: lines.append("└─ depA")
    if depth_limit >= 2: lines.append("   └─ depA1")
    lines.append("└─ depB")
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="Визуализация графа зависимостей (Этап 5)")
    parser.add_argument("--config", default="config.ini", help="Путь к INI-файлу")
    args = parser.parse_args()

    try:
        cfg = load_config(args.config)
    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)

    print("Параметры конфигурации:")
    for k in sorted(cfg.keys()):
        print(f"{k} = {cfg[k]}")

    # Получаем граф зависимостей
    graph = get_dependencies(cfg['package_name'])
    
    mermaid_code = ""
    ascii_tree = ""
    
    if cfg['output_format'] == 'ascii_tree':
        ascii_tree = render_ascii_tree(cfg['package_name'], cfg['max_depth'])
        print("\nASCII-дерево зависимостей:")
        print(ascii_tree)
        
    elif cfg['output_format'] in ('mermaid', 'svg'):
        mermaid_code = generate_mermaid(graph, cfg['max_depth'])
        print("\nСгенерированный Mermaid-код:")
        print(mermaid_code)

    # Создаем выходную папку
    out_dir = os.path.join(os.getcwd(), "ep5_output")
    os.makedirs(out_dir, exist_ok=True)
    
    # Сохраняем результаты
    summary_path = os.path.join(out_dir, "ep5_summary.txt")
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("Этап 5: Визуализация графа зависимостей\n")
        for k in sorted(cfg.keys()):
            f.write(f"{k} = {cfg[k]}\n")
        if ascii_tree:
            f.write("\nASCII-дерево зависимостей:\n" + ascii_tree + "\n")
        if mermaid_code:
            f.write("\nMermaid-код:\n" + mermaid_code + "\n")

    # Если выбран формат svg (или mermaid), сохраняем .mmd и генерируем .svg
    if mermaid_code:
        mmd_path = os.path.join(out_dir, f"{cfg['package_name']}_deps.mmd")
        with open(mmd_path, "w", encoding="utf-8") as f:
            f.write(mermaid_code)
        print(f"Mermaid-файл сохранен: {mmd_path}")

        if cfg['output_format'] == 'svg':
            svg_path = os.path.join(out_dir, f"{cfg['package_name']}_deps.svg")
            print("Генерация SVG...")
            
            # Создаем конфиг для Puppeteer, чтобы он работал без песочницы (sandbox)
            pptr_cfg_path = os.path.join(out_dir, "puppeteer-config.json")
            with open(pptr_cfg_path, "w", encoding="utf-8") as f:
                f.write('{"args": ["--no-sandbox", "--disable-setuid-sandbox"]}')

            # Формируем команду с учетом пробелов в путях (заключаем пути в кавычки)
            cmd = [
                "mmdc",
                "-i", f'"{mmd_path}"',
                "-o", f'"{svg_path}"',
                "-p", f'"{pptr_cfg_path}"'
            ]
            
            try:
                # Запускаем через shell=True, чтобы Windows корректно обработал кавычки
                cmd_str = " ".join(cmd)
                res = subprocess.run(cmd_str, shell=True, capture_output=True, text=True, encoding='utf-8')
                
                if res.returncode == 0:
                    print(f"SVG успешно сохранен: {svg_path}")
                else:
                    print(f"Ошибка при генерации SVG:\n{res.stderr}")
            except Exception as e:
                print(f"Системная ошибка: {e}")

    # Блок Git (оставляем как было)
    cwd = os.getcwd()
    def run(cmd):
        return subprocess.run(cmd, shell=True, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    if not os.path.exists(os.path.join(cwd, ".git")):
        run("git init")
        run("git config user.email 'bot@example.com'")
        run("git config user.name 'SYNTX Bot'")

    run(f'git add "{os.path.relpath(out_dir, cwd)}"')
    status = run("git status --porcelain").stdout.strip()
    if status:
        run("git commit -m 'Etap 5: Визуализация графа зависимостей (Mermaid + SVG)'")
        print("Изменения закоммичены в Git.")
    else:
        print("Нет изменений для коммита.")

if __name__ == "__main__":
    main()