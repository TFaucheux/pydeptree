#!/usr/bin/env python3
"""
Enhanced Python Dependency Tree Analyzer with lint checking and file statistics
"""
import ast
import os
import sys
import subprocess
from pathlib import Path
from typing import Set, Dict, List, Optional, Tuple
from dataclasses import dataclass
import time

import click
from rich.console import Console
from rich.tree import Tree
from rich.panel import Panel
from rich.syntax import Syntax
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich import print as rprint
from rich.text import Text


console = Console()


@dataclass
class FileInfo:
    """Information about a Python file"""
    path: Path
    size: int
    lines: int
    imports: int
    lint_errors: int
    lint_warnings: int
    file_type: str  # 'model', 'service', 'utils', 'test', 'main', 'other'


def detect_file_type(file_path: Path) -> str:
    """Detect the type of Python file based on path and content"""
    path_str = str(file_path).lower()
    
    # Check by directory
    if '/models/' in path_str or '/model/' in path_str:
        return 'model'
    elif '/services/' in path_str or '/service/' in path_str:
        return 'service'
    elif '/utils/' in path_str or '/util/' in path_str:
        return 'utils'
    elif '/tests/' in path_str or '/test/' in path_str or 'test_' in path_str:
        return 'test'
    elif file_path.name == 'main.py' or file_path.name == '__main__.py':
        return 'main'
    
    # Check by filename patterns
    if 'model' in path_str:
        return 'model'
    elif 'service' in path_str or 'api' in path_str or 'client' in path_str:
        return 'service'
    elif 'util' in path_str or 'helper' in path_str or 'config' in path_str:
        return 'utils'
    elif 'test' in path_str:
        return 'test'
    
    return 'other'


def get_file_type_color(file_type: str) -> str:
    """Get color for file type"""
    colors = {
        'model': 'cyan',
        'service': 'green',
        'utils': 'yellow',
        'test': 'magenta',
        'main': 'bold blue',
        'other': 'white'
    }
    return colors.get(file_type, 'white')


def get_file_type_icon(file_type: str) -> str:
    """Get icon for file type"""
    icons = {
        'model': '📊',
        'service': '🌐',
        'utils': '🔧',
        'test': '🧪',
        'main': '🚀',
        'other': '📄'
    }
    return icons.get(file_type, '📄')


def run_ruff_check(file_path: Path) -> Tuple[int, int]:
    """Run ruff on a file and return (errors, warnings)"""
    try:
        result = subprocess.run(
            ['ruff', 'check', str(file_path), '--output-format=json'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            return 0, 0
        
        import json
        try:
            issues = json.loads(result.stdout)
            errors = sum(1 for issue in issues if issue.get('code', '').startswith('E'))
            warnings = len(issues) - errors
            return errors, warnings
        except:
            # If JSON parsing fails, just count by return code
            return 1 if result.returncode != 0 else 0, 0
            
    except (subprocess.TimeoutExpired, FileNotFoundError):
        # Ruff not available or timeout
        return 0, 0


def get_file_info(file_path: Path) -> FileInfo:
    """Get detailed information about a file"""
    try:
        stats = file_path.stat()
        
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            line_count = len(lines)
            
            # Count imports
            import_count = sum(1 for line in lines 
                             if line.strip().startswith(('import ', 'from '))
                             and not line.strip().startswith('#'))
        
        # Run lint check
        errors, warnings = run_ruff_check(file_path)
        
        # Detect file type
        file_type = detect_file_type(file_path)
        
        return FileInfo(
            path=file_path,
            size=stats.st_size,
            lines=line_count,
            imports=import_count,
            lint_errors=errors,
            lint_warnings=warnings,
            file_type=file_type
        )
    except Exception as e:
        console.print(f"[red]Error getting info for {file_path}: {e}[/red]")
        return FileInfo(file_path, 0, 0, 0, 0, 0, 'other')


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


def get_dependencies(file_path: Path, project_root: Path, visited: Set[Path], 
                    max_depth: int, current_depth: int = 0, progress=None,
                    file_info_cache: Dict[Path, FileInfo] = None) -> Dict[Path, Set[Path]]:
    if current_depth >= max_depth or file_path in visited:
        return {}
        
    visited.add(file_path)
    dependencies = {}
    
    if progress:
        progress.update(task_id=0, description=f"Analyzing {file_path.name}")
    
    # Get file info
    if file_info_cache is not None and file_path not in file_info_cache:
        file_info_cache[file_path] = get_file_info(file_path)
    
    imports = parse_imports(file_path, project_root)
    project_imports = {imp for imp in imports if is_project_module(imp, project_root)}
    
    dep_files = set()
    for module in project_imports:
        dep_path = module_to_file_path(module, project_root)
        if dep_path and dep_path != file_path:
            dep_files.add(dep_path)
            # Cache file info for dependencies
            if file_info_cache is not None and dep_path not in file_info_cache:
                file_info_cache[dep_path] = get_file_info(dep_path)
    
    dependencies[file_path] = dep_files
    
    if current_depth + 1 < max_depth:
        for dep_file in dep_files:
            sub_deps = get_dependencies(dep_file, project_root, visited, max_depth, 
                                      current_depth + 1, progress, file_info_cache)
            dependencies.update(sub_deps)
    
    return dependencies


def format_file_label(file_info: FileInfo, project_root: Path) -> Text:
    """Format file label with colors and badges"""
    relative_path = file_info.path.relative_to(project_root) if file_info.path.is_relative_to(project_root) else file_info.path
    
    # Base color based on file type
    color = get_file_type_color(file_info.file_type)
    icon = get_file_type_icon(file_info.file_type)
    
    label = Text()
    label.append(f"{icon} ", style=color)
    label.append(str(relative_path), style=color)
    
    # Add badges
    badges = []
    
    # Size badge
    if file_info.size < 1024:
        size_str = f"{file_info.size}B"
    elif file_info.size < 1024 * 1024:
        size_str = f"{file_info.size / 1024:.1f}KB"
    else:
        size_str = f"{file_info.size / (1024 * 1024):.1f}MB"
    badges.append(f"[dim]{size_str}[/dim]")
    
    # Lines badge
    badges.append(f"[dim]{file_info.lines}L[/dim]")
    
    # Imports badge
    if file_info.imports > 0:
        badges.append(f"[cyan]{file_info.imports}↓[/cyan]")
    
    # Lint badges
    if file_info.lint_errors > 0:
        badges.append(f"[red]E:{file_info.lint_errors}[/red]")
    if file_info.lint_warnings > 0:
        badges.append(f"[yellow]W:{file_info.lint_warnings}[/yellow]")
    
    if badges:
        label.append(" ")
        label.append(" ".join(badges))
    
    return label


def build_rich_tree(file_path: Path, dependencies: Dict[Path, Set[Path]], 
                   project_root: Path, file_info_cache: Dict[Path, FileInfo],
                   tree: Tree = None, visited: Set[Path] = None):
    if visited is None:
        visited = set()
        
    if file_path in visited:
        return
        
    visited.add(file_path)
    
    file_info = file_info_cache.get(file_path, FileInfo(file_path, 0, 0, 0, 0, 0, 'other'))
    label = format_file_label(file_info, project_root)
    
    if tree is None:
        tree = Tree(label)
        current_node = tree
    else:
        current_node = tree.add(label)
    
    if file_path in dependencies:
        deps = sorted(dependencies[file_path])
        for dep in deps:
            if dep not in visited:
                build_rich_tree(dep, dependencies, project_root, file_info_cache, current_node, visited)
            else:
                dep_info = file_info_cache.get(dep, FileInfo(dep, 0, 0, 0, 0, 0, 'other'))
                circular_label = format_file_label(dep_info, project_root)
                circular_label.append(" [dim](circular)[/dim]")
                current_node.add(circular_label)
    
    return tree


def create_summary_table(file_info_cache: Dict[Path, FileInfo]) -> Table:
    """Create a summary table of file statistics"""
    table = Table(title="File Statistics Summary")
    
    table.add_column("Type", style="cyan", width=10)
    table.add_column("Count", justify="right", style="green")
    table.add_column("Total Lines", justify="right", style="yellow")
    table.add_column("Avg Lines", justify="right", style="yellow")
    table.add_column("Errors", justify="right", style="red")
    table.add_column("Warnings", justify="right", style="yellow")
    
    # Group by file type
    type_stats = {}
    for file_info in file_info_cache.values():
        if file_info.file_type not in type_stats:
            type_stats[file_info.file_type] = {
                'count': 0,
                'lines': 0,
                'errors': 0,
                'warnings': 0
            }
        
        stats = type_stats[file_info.file_type]
        stats['count'] += 1
        stats['lines'] += file_info.lines
        stats['errors'] += file_info.lint_errors
        stats['warnings'] += file_info.lint_warnings
    
    # Add rows to table
    for file_type, stats in sorted(type_stats.items()):
        icon = get_file_type_icon(file_type)
        avg_lines = stats['lines'] // stats['count'] if stats['count'] > 0 else 0
        
        table.add_row(
            f"{icon} {file_type}",
            str(stats['count']),
            str(stats['lines']),
            str(avg_lines),
            str(stats['errors']) if stats['errors'] > 0 else "-",
            str(stats['warnings']) if stats['warnings'] > 0 else "-"
        )
    
    # Add total row
    total_count = sum(s['count'] for s in type_stats.values())
    total_lines = sum(s['lines'] for s in type_stats.values())
    total_errors = sum(s['errors'] for s in type_stats.values())
    total_warnings = sum(s['warnings'] for s in type_stats.values())
    
    table.add_section()
    table.add_row(
        "[bold]Total[/bold]",
        f"[bold]{total_count}[/bold]",
        f"[bold]{total_lines}[/bold]",
        f"[bold]{total_lines // total_count if total_count > 0 else 0}[/bold]",
        f"[bold red]{total_errors}[/bold red]" if total_errors > 0 else "[bold]-[/bold]",
        f"[bold yellow]{total_warnings}[/bold yellow]" if total_warnings > 0 else "[bold]-[/bold]"
    )
    
    return table


@click.command()
@click.argument('file_path', type=click.Path(exists=True, path_type=Path))
@click.option('--depth', '-d', default=1, help='Maximum depth to traverse dependencies (default: 1)')
@click.option('--project-root', '-r', type=click.Path(exists=True, path_type=Path), 
              help='Project root directory (default: parent directory of the file)')
@click.option('--show-code', '-c', is_flag=True, help='Show import statements from each file')
@click.option('--check-lint/--no-check-lint', '-l', default=True, help='Check for lint errors (default: enabled)')
@click.option('--show-stats/--no-show-stats', '-s', default=True, help='Show file statistics summary (default: enabled)')
def main(file_path: Path, depth: int, project_root: Path, show_code: bool, check_lint: bool, show_stats: bool):
    """
    Enhanced Python Dependency Analyzer with lint checking and file statistics.
    
    FILE_PATH: Path to the Python file to analyze
    
    Features:
    - Color-coded file types (models, services, utils, tests, main)
    - Lint error/warning detection using ruff
    - File statistics (size, lines, imports)
    - Summary statistics table
    """
    if not file_path.suffix == '.py':
        console.print("[red]Error: File must be a Python file (.py)[/red]")
        sys.exit(1)
    
    if project_root is None:
        project_root = file_path.parent
    
    # Check if ruff is available
    if check_lint:
        try:
            subprocess.run(['ruff', '--version'], capture_output=True, timeout=1)
        except (subprocess.TimeoutExpired, FileNotFoundError):
            console.print("[yellow]Warning: ruff not found, lint checking disabled[/yellow]")
            check_lint = False
    
    # Display header
    console.print(Panel.fit(
        f"[bold]Enhanced Python Dependency Analyzer[/bold]\n\n"
        f"File: [cyan]{file_path}[/cyan]\n"
        f"Project root: [cyan]{project_root}[/cyan]\n"
        f"Max depth: [yellow]{depth}[/yellow]\n"
        f"Lint checking: [{'green' if check_lint else 'red'}]{'enabled' if check_lint else 'disabled'}[/{'green' if check_lint else 'red'}]",
        title="Analysis Settings"
    ))
    
    # Legend
    console.print("\n[bold]Legend:[/bold]")
    legend_items = [
        f"{get_file_type_icon('model')} Models",
        f"{get_file_type_icon('service')} Services",
        f"{get_file_type_icon('utils')} Utils",
        f"{get_file_type_icon('test')} Tests",
        f"{get_file_type_icon('main')} Main",
        "[dim]Size[/dim]",
        "[dim]Lines[/dim]",
        "[cyan]Imports↓[/cyan]",
        "[red]E:Errors[/red]",
        "[yellow]W:Warnings[/yellow]"
    ]
    console.print(" | ".join(legend_items))
    
    file_info_cache = {}
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True
    ) as progress:
        task_id = progress.add_task("Analyzing dependencies...", total=None)
        
        visited = set()
        dependencies = get_dependencies(file_path, project_root, visited, depth, 
                                      progress=progress, file_info_cache=file_info_cache)
    
    # Build and display tree
    tree = build_rich_tree(file_path, dependencies, project_root, file_info_cache)
    console.print("\n")
    console.print(Panel(tree, title="[bold]Dependency Tree[/bold]", expand=False))
    
    # Show statistics
    total_files = len(dependencies)
    total_deps = sum(len(deps) for deps in dependencies.values())
    console.print(f"\n[dim]Found {total_files} files with {total_deps} total dependencies[/dim]")
    
    # Show summary table
    if show_stats and file_info_cache:
        console.print("\n")
        console.print(create_summary_table(file_info_cache))
    
    # Show files with lint issues
    if check_lint:
        files_with_errors = [(f, info) for f, info in file_info_cache.items() 
                           if info.lint_errors > 0]
        files_with_warnings = [(f, info) for f, info in file_info_cache.items() 
                             if info.lint_warnings > 0 and info.lint_errors == 0]
        
        if files_with_errors or files_with_warnings:
            console.print("\n[bold]Lint Issues:[/bold]")
            
            if files_with_errors:
                console.print("\n[red]Files with errors:[/red]")
                for file_path, info in sorted(files_with_errors, 
                                            key=lambda x: x[1].lint_errors, 
                                            reverse=True):
                    rel_path = file_path.relative_to(project_root) if file_path.is_relative_to(project_root) else file_path
                    console.print(f"  [red]✗[/red] {rel_path} - {info.lint_errors} error(s)")
            
            if files_with_warnings:
                console.print("\n[yellow]Files with warnings:[/yellow]")
                for file_path, info in sorted(files_with_warnings, 
                                            key=lambda x: x[1].lint_warnings, 
                                            reverse=True)[:5]:  # Show top 5
                    rel_path = file_path.relative_to(project_root) if file_path.is_relative_to(project_root) else file_path
                    console.print(f"  [yellow]⚠[/yellow]  {rel_path} - {info.lint_warnings} warning(s)")
    
    # Optionally show import statements
    if show_code and dependencies:
        console.print("\n[bold]Import Statements:[/bold]\n")
        for file, deps in sorted(dependencies.items()):
            if deps:
                rel_path = file.relative_to(project_root) if file.is_relative_to(project_root) else file
                file_info = file_info_cache.get(file)
                color = get_file_type_color(file_info.file_type) if file_info else 'white'
                console.print(f"[bold {color}]{rel_path}:[/bold {color}]")
                
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