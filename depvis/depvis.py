import configparser
import sys
import urllib.request
import json
from collections import deque

class DependencyVisualizer:
    def __init__(self, config_file):
        self.config = configparser.ConfigParser()
        self.config.read(config_file, encoding='utf-8')

        self.package_name = self.config.get('Settings', 'package_name')
        self.repo_url = self.config.get('Settings', 'repo_url')
        self.test_mode = self.config.getboolean('Settings', 'test_mode')
        self.package_version = self.config.get('Settings', 'package_version')
        self.ascii_tree = self.config.getboolean('Settings', 'ascii_tree')
        self.max_depth = self.config.getint('Settings', 'max_depth')

        self.graph = {}
        self.all_deps = set()

    def fetch_package_info(self, package, version):
        if self.test_mode:
            with open(self.repo_url, 'r', encoding='utf-8') as f:
                data = json.load(f)
                key = f"{package}=={version}"
                if key in data:
                    return data[key]
                return None
        else:
            url = f"{self.repo_url}/{package}/{version}/json"
            try:
                with urllib.request.urlopen(url) as response:
                    data = json.load(response)
                    return data.get('info', {}).get('requires_dist', [])
            except:
                return None

    def parse_dependency(self, dep_string):
        if not dep_string:
            return None, None
        dep_string = dep_string.split(';')[0].strip()
        if '==' in dep_string:
            name, version = dep_string.split('==')
            return name.strip(), version.strip()
        elif '>=' in dep_string:
            name = dep_string.split('>=')[0].strip()
            return name, None
        else:
            parts = dep_string.split()
            if parts:
                return parts[0].strip(), None
        return None, None

    def build_graph_dfs(self):
        visited = set()
        stack = [(self.package_name, self.package_version, 0)]

        while stack:
            pkg, ver, depth = stack.pop()

            if depth > self.max_depth:
                continue

            key = f"{pkg}=={ver}" if ver else pkg
            if key in visited:
                continue
            visited.add(key)

            deps_info = self.fetch_package_info(pkg, ver)
            if deps_info is None:
                self.graph[key] = []
                continue

            dependencies = []
            if isinstance(deps_info, list):
                for dep in deps_info:
                    name, version = self.parse_dependency(dep)
                    if name:
                        dep_key = f"{name}=={version}" if version else name
                        dependencies.append(dep_key)
                        self.all_deps.add(dep_key)
                        if depth < self.max_depth:
                            stack.append((name, version, depth + 1))

            self.graph[key] = dependencies

    def find_reverse_dependencies(self, target_package):
        reverse_deps = []
        for pkg, deps in self.graph.items():
            for dep in deps:
                dep_name = dep.split('==')[0]
                target_name = target_package.split('==')[0]
                if dep_name == target_name:
                    reverse_deps.append(pkg)
                    break
        return reverse_deps

    def detect_cycles(self):
        cycles = []

        def dfs_cycle(node, path, visited_in_path):
            if node in visited_in_path:
                cycle_start = path.index(node)
                cycles.append(path[cycle_start:] + [node])
                return

            if node not in self.graph:
                return

            visited_in_path.add(node)
            path.append(node)

            for neighbor in self.graph[node]:
                dfs_cycle(neighbor, path[:], visited_in_path.copy())

        for node in self.graph:
            dfs_cycle(node, [], set())

        return cycles

    def generate_ascii_tree(self):
        lines = []
        root = f"{self.package_name}=={self.package_version}"

        def print_tree(node, prefix="", is_last=True, visited=None):
            if visited is None:
                visited = set()

            if node in visited:
                lines.append(f"{prefix}{'└── ' if is_last else '├── '}{node} (circular)")
                return

            visited.add(node)
            lines.append(f"{prefix}{'└── ' if is_last else '├── '}{node}")

            if node not in self.graph:
                return

            children = self.graph[node]
            for i, child in enumerate(children):
                is_last_child = (i == len(children) - 1)
                extension = "    " if is_last else "│   "
                print_tree(child, prefix + extension, is_last_child, visited.copy())

        print_tree(root)
        return "\n".join(lines)

    def generate_d2_diagram(self):
        lines = ["direction: right"]

        for pkg, deps in self.graph.items():
            pkg_clean = pkg.replace('-', '_').replace('.', '_').replace('==', '_')
            lines.append(f'{pkg_clean}: "{pkg}"')
            for dep in deps:
                dep_clean = dep.replace('-', '_').replace('.', '_').replace('==', '_')
                lines.append(f'{pkg_clean} -> {dep_clean}')

        return "\n".join(lines)

    def run(self):
        print(f"package_name={self.package_name}")
        print(f"repo_url={self.repo_url}")
        print(f"test_mode={self.test_mode}")
        print(f"package_version={self.package_version}")
        print(f"ascii_tree={self.ascii_tree}")
        print(f"max_depth={self.max_depth}")
        print()

        print("Building dependency graph...")
        self.build_graph_dfs()

        print(f"\nDirect dependencies of {self.package_name}=={self.package_version}:")
        root_key = f"{self.package_name}=={self.package_version}"
        if root_key in self.graph:
            for dep in self.graph[root_key]:
                print(f"  - {dep}")

        print("\nReverse dependencies:")
        reverse_deps = self.find_reverse_dependencies(root_key)
        for rdep in reverse_deps:
            print(f"  - {rdep}")

        cycles = self.detect_cycles()
        if cycles:
            print("\nCycles detected:")
            for cycle in cycles[:5]:
                print("  " + " -> ".join(cycle))
        else:
            print("\nNo cycles detected")

        if self.ascii_tree:
            print("\nASCII Tree:")
            print(self.generate_ascii_tree())

        print("\nD2 Diagram:")
        print(self.generate_d2_diagram())

if __name__ == "__main__":
    if len(sys.argv) > 1:
        config_file = sys.argv[1]
    else:
        config_file = "config.ini"

    visualizer = DependencyVisualizer(config_file)
    visualizer.run()
