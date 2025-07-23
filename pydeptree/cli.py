#!/usr/bin/env python3
"""
Python Dependency Tree Analyzer - Rich version with enhanced UI
"""
import ast
import os
import sys
from pathlib import Path
from typing import Set, Dict, List, Optional

import click
from rich.console import Console
from rich.tree import Tree
from rich.panel import Panel
from rich.syntax import Syntax
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print as rprint


console = Console()


class ImportVisitor(ast.NodeVisitor):
    def __init__(self, project_root: Path):
        self.imports: Set[str] = set()
        self.project_root = project_root
        
    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            self.imports.add(alias.name)
        self.generic_visit(node)
        
    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        if node.module:
            self.imports.add(node.module)
        self.generic_visit(node)


def parse_imports(file_path: Path, project_root: Path) -> Set[str]:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            tree = ast.parse(content)
        
        visitor = ImportVisitor(project_root)
        visitor.visit(tree)
        return visitor.imports
    except Exception as e:
        console.print(f"[red]Error parsing {file_path}: {e}[/red]")
        return set()


def is_project_module(module_name: str, project_root: Path) -> bool:
    parts = module_name.split('.')
    
    for i in range(len(parts), 0, -1):
        potential_path = project_root / Path(*parts[:i])
        
        if potential_path.with_suffix('.py').exists():
            return True
        
        if potential_path.is_dir() and (potential_path / '__init__.py').exists():
            return True
            
    return False


def module_to_file_path(module_name: str, project_root: Path) -> Optional[Path]:
    parts = module_name.split('.')
    
    for i in range(len(parts), 0, -1):
        potential_path = project_root / Path(*parts[:i])
        
        py_file = potential_path.with_suffix('.py')
        if py_file.exists():
            return py_file
        
        init_file = potential_path / '__init__.py'
        if init_file.exists():
            return init_file
            
    return None


def get_dependencies(file_path: Path, project_root: Path, visited: Set[Path], max_depth: int, current_depth: int = 0, progress=None) -> Dict[Path, Set[Path]]:
    if current_depth >= max_depth or file_path in visited:
        return {}
        
    visited.add(file_path)
    dependencies = {}
    
    if progress:
        progress.update(task_id=0, description=f"Analyzing {file_path.name}")
    
    imports = parse_imports(file_path, project_root)
    project_imports = {imp for imp in imports if is_project_module(imp, project_root)}
    
    dep_files = set()
    for module in project_imports:
        dep_path = module_to_file_path(module, project_root)
        if dep_path and dep_path != file_path:
            dep_files.add(dep_path)
    
    dependencies[file_path] = dep_files
    
    if current_depth + 1 < max_depth:
        for dep_file in dep_files:
            sub_deps = get_dependencies(dep_file, project_root, visited, max_depth, current_depth + 1, progress)
            dependencies.update(sub_deps)
    
    return dependencies


def build_rich_tree(file_path: Path, dependencies: Dict[Path, Set[Path]], project_root: Path, tree: Tree = None, visited: Set[Path] = None):
    if visited is None:
        visited = set()
        
    if file_path in visited:
        return
        
    visited.add(file_path)
    
    relative_path = file_path.relative_to(project_root) if file_path.is_relative_to(project_root) else file_path
    
    if tree is None:
        tree = Tree(f"[bold blue]{relative_path}[/bold blue]")
        current_node = tree
    else:
        current_node = tree.add(f"[green]{relative_path}[/green]")
    
    if file_path in dependencies:
        deps = sorted(dependencies[file_path])
        for dep in deps:
            if dep not in visited:
                build_rich_tree(dep, dependencies, project_root, current_node, visited)
            else:
                current_node.add(f"[dim]{dep.relative_to(project_root)} (circular)[/dim]")
    
    return tree


@click.command()
@click.argument('file_path', type=click.Path(exists=True, path_type=Path))
@click.option('--depth', '-d', default=1, help='Maximum depth to traverse dependencies (default: 1)')
@click.option('--project-root', '-r', type=click.Path(exists=True, path_type=Path), 
              help='Project root directory (default: parent directory of the file)')
@click.option('--show-code', '-c', is_flag=True, help='Show import statements from each file')
def main(file_path: Path, depth: int, project_root: Path, show_code: bool):
    """
    Analyze Python file dependencies and display them as a tree with rich formatting.
    
    FILE_PATH: Path to the Python file to analyze
    """
    if not file_path.suffix == '.py':
        console.print("[red]Error: File must be a Python file (.py)[/red]")
        sys.exit(1)
    
    if project_root is None:
        project_root = file_path.parent
    
    # Display header
    console.print(Panel.fit(
        f"[bold]Python Dependency Analyzer[/bold]\n\n"
        f"File: [cyan]{file_path}[/cyan]\n"
        f"Project root: [cyan]{project_root}[/cyan]\n"
        f"Max depth: [yellow]{depth}[/yellow]",
        title="Analysis Settings"
    ))
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True
    ) as progress:
        task_id = progress.add_task("Analyzing dependencies...", total=None)
        
        visited = set()
        dependencies = get_dependencies(file_path, project_root, visited, depth, progress=progress)
    
    # Build and display tree
    tree = build_rich_tree(file_path, dependencies, project_root)
    console.print("\n")
    console.print(Panel(tree, title="[bold]Dependency Tree[/bold]", expand=False))
    
    # Show statistics
    total_files = len(dependencies)
    total_deps = sum(len(deps) for deps in dependencies.values())
    console.print(f"\n[dim]Found {total_files} files with {total_deps} total dependencies[/dim]")
    
    # Optionally show import statements
    if show_code and dependencies:
        console.print("\n[bold]Import Statements:[/bold]\n")
        for file, deps in sorted(dependencies.items()):
            if deps:
                rel_path = file.relative_to(project_root) if file.is_relative_to(project_root) else file
                console.print(f"[bold cyan]{rel_path}:[/bold cyan]")
                
                with open(file, 'r') as f:
                    lines = f.readlines()
                    import_lines = []
                    for i, line in enumerate(lines, 1):
                        if line.strip().startswith(('import ', 'from ')) and any(
                            str(dep.stem) in line for dep in deps
                        ):
                            import_lines.append((i, line.rstrip()))
                    
                    for line_no, line in import_lines:
                        console.print(f"  [dim]{line_no:4d}:[/dim] {line}")
                console.print()


if __name__ == '__main__':
    main()