#!/usr/bin/env python3
"""
Advanced Python Dependency Tree Analyzer with search, complexity metrics, and more
"""
import ast
import os
import sys
import subprocess
import re
from pathlib import Path
from typing import Set, Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
import time
from datetime import datetime

import click
from rich.console import Console
from rich.tree import Tree
from rich.panel import Panel
from rich.syntax import Syntax
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich import print as rprint
from rich.text import Text
from rich.highlighter import RegexHighlighter
from rich.prompt import Prompt, Confirm


console = Console()


class SearchHighlighter(RegexHighlighter):
    """Highlighter for search results"""
    def __init__(self, search_pattern: str):
        self.search_pattern = search_pattern
        super().__init__()
        
    @property
    def highlights(self):
        return [self.search_pattern]


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
    complexity: int = 0  # Cyclomatic complexity
    functions: int = 0  # Number of functions
    classes: int = 0  # Number of classes
    todos: List[Tuple[int, str]] = field(default_factory=list)  # Line number and TODO text
    git_status: Optional[str] = None  # Git status (M, A, D, etc.)
    search_matches: List[Tuple[int, str]] = field(default_factory=list)  # Search results


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
    elif 'main.py' in path_str or '__main__.py' in path_str:
        return 'main'
    else:
        return 'other'


def get_file_type_color(file_type: str) -> str:
    """Get color for file type"""
    colors = {
        'model': 'cyan',
        'service': 'green',
        'utils': 'yellow',
        'test': 'magenta',
        'main': 'red',
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


def calculate_complexity(tree: ast.AST) -> int:
    """Calculate cyclomatic complexity of an AST"""
    complexity = 1  # Base complexity
    
    for node in ast.walk(tree):
        if isinstance(node, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
            complexity += 1
        elif isinstance(node, ast.BoolOp):
            complexity += len(node.values) - 1
        elif isinstance(node, ast.comprehension):
            complexity += sum(1 for _ in node.ifs) + 1
            
    return complexity


def count_functions_and_classes(tree: ast.AST) -> Tuple[int, int]:
    """Count functions and classes in an AST"""
    functions = 0
    classes = 0
    
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            functions += 1
        elif isinstance(node, ast.ClassDef):
            classes += 1
            
    return functions, classes


def find_todos(content: str) -> List[Tuple[int, str]]:
    """Find TODO/FIXME/HACK comments in file content"""
    todos = []
    patterns = [
        r'#\s*(TODO|FIXME|HACK|XXX|NOTE|OPTIMIZE|BUG):?\s*(.*)',
        r'""".*?(TODO|FIXME|HACK|XXX|NOTE|OPTIMIZE|BUG):?\s*(.*?)"""',
        r"'''.*?(TODO|FIXME|HACK|XXX|NOTE|OPTIMIZE|BUG):?\s*(.*?)'''"
    ]
    
    lines = content.split('\n')
    for i, line in enumerate(lines, 1):
        for pattern in patterns:
            matches = re.finditer(pattern, line, re.IGNORECASE)
            for match in matches:
                todo_type = match.group(1).upper()
                todo_text = match.group(2).strip() if match.lastindex >= 2 else ""
                todos.append((i, f"{todo_type}: {todo_text}"))
                
    return todos


def search_in_file(file_path: Path, search_pattern: str, search_type: str) -> List[Tuple[int, str]]:
    """Search for pattern in file and return matches with line numbers"""
    matches = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Build pattern based on search type
        if search_type == 'class':
            pattern = rf'class\s+{search_pattern}'
        elif search_type == 'function':
            pattern = rf'def\s+{search_pattern}'
        elif search_type == 'import':
            pattern = rf'(from|import).*{search_pattern}'
        else:
            pattern = search_pattern
            
        # Search line by line
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            if re.search(pattern, line, re.IGNORECASE if search_type == 'text' else 0):
                matches.append((i, line.strip()))
                
    except Exception:
        pass
        
    return matches


def get_git_status(file_path: Path, project_root: Path) -> Optional[str]:
    """Get git status for a file"""
    try:
        # Find git root by looking for .git directory
        git_root = project_root
        while git_root.parent != git_root:
            if (git_root / '.git').exists():
                break
            git_root = git_root.parent
        else:
            # No .git found, try current directory
            if not (git_root / '.git').exists():
                return None
                
        # Get relative path from git root
        try:
            rel_path = file_path.relative_to(git_root)
        except ValueError:
            # File is outside git repository
            return None
            
        # Run git status for the specific file
        result = subprocess.run(
            ['git', 'status', '--porcelain', str(rel_path)],
            cwd=git_root,
            capture_output=True,
            text=True,
            timeout=1
        )
        
        if result.returncode == 0 and result.stdout:
            # Git status format: XY filename
            # X = staged status, Y = unstaged status
            status = result.stdout.strip()[:2].strip()
            if status:
                return status
                
    except Exception:
        pass
        
    return None


def run_ruff_check(file_path: Path) -> Tuple[int, int]:
    """Run ruff linter on a file and return error/warning counts"""
    try:
        result = subprocess.run(
            ['ruff', 'check', str(file_path), '--output-format=json'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.stdout:
            import json
            issues = json.loads(result.stdout)
            errors = sum(1 for issue in issues if issue.get('type') == 'error' or 'E' in issue.get('code', ''))
            warnings = len(issues) - errors
            return errors, warnings
    except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
        pass
    
    return 0, 0


def analyze_file(file_path: Path, project_root: Path, search_pattern: Optional[str] = None, 
                search_type: str = 'text', check_git: bool = True) -> FileInfo:
    """Analyze a Python file and return file information"""
    try:
        stat = file_path.stat()
        size = stat.st_size
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = len(content.splitlines())
            
        # Parse AST
        try:
            tree = ast.parse(content)
            imports = sum(1 for node in ast.walk(tree) 
                         if isinstance(node, (ast.Import, ast.ImportFrom)))
            complexity = calculate_complexity(tree)
            functions, classes = count_functions_and_classes(tree)
        except:
            imports = 0
            complexity = 0
            functions = 0
            classes = 0
            
        # Find TODOs
        todos = find_todos(content)
        
        # Search if pattern provided
        search_matches = []
        if search_pattern:
            search_matches = search_in_file(file_path, search_pattern, search_type)
            
        # Get git status
        git_status = None
        if check_git:
            git_status = get_git_status(file_path, project_root)
            
        # Run linter
        errors, warnings = run_ruff_check(file_path)
        
        return FileInfo(
            path=file_path,
            size=size,
            lines=lines,
            imports=imports,
            lint_errors=errors,
            lint_warnings=warnings,
            file_type=detect_file_type(file_path),
            complexity=complexity,
            functions=functions,
            classes=classes,
            todos=todos,
            git_status=git_status,
            search_matches=search_matches
        )
    except Exception as e:
        # Return minimal info on error
        return FileInfo(
            path=file_path,
            size=0,
            lines=0,
            imports=0,
            lint_errors=0,
            lint_warnings=0,
            file_type=detect_file_type(file_path),
            complexity=0,
            functions=0,
            classes=0,
            todos=[],
            git_status=None,
            search_matches=[]
        )


def format_file_label(file_info: FileInfo, project_root: Path, show_metrics: bool = True) -> Text:
    """Format file label with colors and badges"""
    relative_path = file_info.path.relative_to(project_root) if file_info.path.is_relative_to(project_root) else file_info.path
    
    # Base color based on file type
    color = get_file_type_color(file_info.file_type)
    icon = get_file_type_icon(file_info.file_type)
    
    label = Text()
    label.append(f"{icon} ", style=color)
    label.append(str(relative_path), style=color)
    
    if show_metrics:
        # Add badges with proper Text styling
        if file_info.size > 0 or file_info.lines > 0:
            label.append(" ")
            
            # Size badge
            if file_info.size < 1024:
                size_str = f"{file_info.size}B"
            elif file_info.size < 1024 * 1024:
                size_str = f"{file_info.size / 1024:.1f}KB"
            else:
                size_str = f"{file_info.size / (1024 * 1024):.1f}MB"
            label.append(size_str, style="dim")
            
            # Lines and imports
            if file_info.lines > 0:
                label.append(f" {file_info.lines}L", style="dim")
            if file_info.imports > 0:
                label.append(f" {file_info.imports}↓", style="dim")
                
            # Complexity
            if file_info.complexity > 10:
                label.append(f" C:{file_info.complexity}", style="bold red")
            elif file_info.complexity > 5:
                label.append(f" C:{file_info.complexity}", style="yellow")
            elif file_info.complexity > 0:
                label.append(f" C:{file_info.complexity}", style="dim")
                
            # Functions and classes
            if file_info.functions > 0 or file_info.classes > 0:
                label.append(f" [{file_info.classes}c/{file_info.functions}f]", style="dim cyan")
                
            # Lint issues
            if file_info.lint_errors > 0:
                label.append(f" E:{file_info.lint_errors}", style="bold red")
            if file_info.lint_warnings > 0:
                label.append(f" W:{file_info.lint_warnings}", style="yellow")
                
            # TODOs
            if file_info.todos:
                label.append(f" 📌{len(file_info.todos)}", style="bright_blue")
                
            # Git status
            if file_info.git_status:
                git_style = "red" if file_info.git_status in ['M', 'MM'] else "green"
                label.append(f" [{file_info.git_status}]", style=git_style)
                
            # Search matches
            if file_info.search_matches:
                label.append(f" 🔍{len(file_info.search_matches)}", style="bold magenta")
    
    return label


def get_python_files_in_directory(directory: Path, seen: Set[Path]) -> List[Path]:
    """Get all Python files in a directory"""
    python_files = []
    
    try:
        for item in directory.iterdir():
            if item.name.startswith('.'):
                continue
                
            if item.is_file() and item.suffix == '.py':
                abs_path = item.resolve()
                if abs_path not in seen:
                    python_files.append(item)
                    seen.add(abs_path)
                    
    except PermissionError:
        pass
        
    return python_files


def extract_imports(file_path: Path) -> Set[str]:
    """Extract all imports from a Python file"""
    imports = set()
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read())
            
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.add(node.module)
                    
    except Exception:
        pass
        
    return imports


def extract_external_dependencies(file_stats: Dict[str, FileInfo], project_root: Path) -> Dict[str, Set[str]]:
    """Extract external (non-project) dependencies from all analyzed files"""
    external_deps = {}
    
    # Get all project module names
    project_modules = set()
    for file_path_str in file_stats:
        file_path = Path(file_path_str)
        try:
            rel_path = file_path.relative_to(project_root)
            # Convert file path to module name
            module_parts = list(rel_path.parts[:-1])  # Remove filename
            if rel_path.stem != '__init__':
                module_parts.append(rel_path.stem)
            if module_parts:
                project_modules.add(module_parts[0])  # Top-level package
        except ValueError:
            pass
    
    # Analyze each file for external imports
    for file_path_str, file_info in file_stats.items():
        file_path = Path(file_path_str)
        imports = extract_imports(file_path)
        
        file_external_deps = set()
        for imp in imports:
            # Get top-level module name
            top_level = imp.split('.')[0]
            
            # Check if it's external (not in stdlib, not project module)
            if top_level not in project_modules and not is_stdlib_module(top_level):
                file_external_deps.add(top_level)
        
        if file_external_deps:
            external_deps[str(file_path)] = file_external_deps
    
    return external_deps


def is_stdlib_module(module_name: str) -> bool:
    """Check if a module is part of Python standard library"""
    stdlib_modules = {
        'abc', 'aifc', 'argparse', 'array', 'ast', 'asynchat', 'asyncio', 'asyncore',
        'atexit', 'audioop', 'base64', 'bdb', 'binascii', 'binhex', 'bisect', 'builtins',
        'bz2', 'calendar', 'cgi', 'cgitb', 'chunk', 'cmath', 'cmd', 'code', 'codecs',
        'codeop', 'collections', 'colorsys', 'compileall', 'concurrent', 'configparser',
        'contextlib', 'contextvars', 'copy', 'copyreg', 'crypt', 'csv', 'ctypes', 'curses',
        'dataclasses', 'datetime', 'dbm', 'decimal', 'difflib', 'dis', 'distutils',
        'doctest', 'dummy_threading', 'email', 'encodings', 'ensurepip', 'enum', 'errno',
        'faulthandler', 'fcntl', 'filecmp', 'fileinput', 'fnmatch', 'formatter', 'fractions',
        'ftplib', 'functools', 'gc', 'getopt', 'getpass', 'gettext', 'glob', 'grp', 'gzip',
        'hashlib', 'heapq', 'hmac', 'html', 'http', 'imaplib', 'imghdr', 'imp', 'importlib',
        'inspect', 'io', 'ipaddress', 'itertools', 'json', 'keyword', 'lib2to3', 'linecache',
        'locale', 'logging', 'lzma', 'mailbox', 'mailcap', 'marshal', 'math', 'mimetypes',
        'mmap', 'modulefinder', 'msilib', 'msvcrt', 'multiprocessing', 'netrc', 'nis',
        'nntplib', 'numbers', 'operator', 'optparse', 'os', 'ossaudiodev', 'parser', 'pathlib',
        'pdb', 'pickle', 'pickletools', 'pipes', 'pkgutil', 'platform', 'plistlib', 'poplib',
        'posix', 'posixpath', 'pprint', 'profile', 'pstats', 'pty', 'pwd', 'py_compile',
        'pyclbr', 'pydoc', 'queue', 'quopri', 'random', 're', 'readline', 'reprlib',
        'resource', 'rlcompleter', 'runpy', 'sched', 'secrets', 'select', 'selectors',
        'shelve', 'shlex', 'shutil', 'signal', 'site', 'smtpd', 'smtplib', 'sndhdr',
        'socket', 'socketserver', 'spwd', 'sqlite3', 'ssl', 'stat', 'statistics', 'string',
        'stringprep', 'struct', 'subprocess', 'sunau', 'symbol', 'symtable', 'sys',
        'sysconfig', 'syslog', 'tabnanny', 'tarfile', 'telnetlib', 'tempfile', 'termios',
        'test', 'textwrap', 'threading', 'time', 'timeit', 'tkinter', 'token', 'tokenize',
        'trace', 'traceback', 'tracemalloc', 'tty', 'turtle', 'types', 'typing', 'unicodedata',
        'unittest', 'urllib', 'uu', 'uuid', 'venv', 'warnings', 'wave', 'weakref',
        'webbrowser', 'winreg', 'winsound', 'wsgiref', 'xdrlib', 'xml', 'xmlrpc', 'zipapp',
        'zipfile', 'zipimport', 'zlib', '_thread', '__future__'
    }
    return module_name in stdlib_modules


def get_package_info(package_name: str) -> Dict[str, Optional[str]]:
    """Get detailed package information including version, summary, and dependencies"""
    info = {
        'version': None,
        'summary': None,
        'requires': [],
        'home_page': None,
        'author': None
    }
    
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'show', package_name],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            current_key = None
            for line in result.stdout.split('\n'):
                line = line.strip()
                if ':' in line and not line.startswith(' '):
                    key, value = line.split(':', 1)
                    key = key.strip().lower().replace('-', '_')
                    value = value.strip()
                    
                    if key == 'version':
                        info['version'] = value
                    elif key == 'summary':
                        info['summary'] = value
                    elif key == 'requires':
                        if value:
                            # Parse requirements, handling version specifiers
                            reqs = [req.strip() for req in value.split(',') if req.strip()]
                            info['requires'] = reqs
                        else:
                            info['requires'] = []
                    elif key == 'home_page':
                        info['home_page'] = value
                    elif key == 'author':
                        info['author'] = value
                        
    except Exception:
        pass
    
    return info


def get_installed_package_version(package_name: str) -> Optional[str]:
    """Get the installed version of a package"""
    info = get_package_info(package_name)
    return info.get('version')


def generate_requirements_content(external_deps: Dict[str, Set[str]], 
                                include_versions: bool = True,
                                add_comments: bool = True) -> str:
    """Generate requirements.txt content from external dependencies"""
    # Collect all unique dependencies
    all_deps = set()
    dep_to_files = {}
    
    for file_path, deps in external_deps.items():
        for dep in deps:
            all_deps.add(dep)
            if dep not in dep_to_files:
                dep_to_files[dep] = []
            dep_to_files[dep].append(file_path)
    
    # Sort dependencies
    sorted_deps = sorted(all_deps)
    
    # Build content
    lines = []
    
    if add_comments:
        lines.append(f"# Generated by PyDepTree on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"# Found {len(sorted_deps)} external dependencies in {len(external_deps)} files")
        lines.append("")
    
    for dep in sorted_deps:
        if include_versions:
            version = get_installed_package_version(dep)
            if version:
                line = f"{dep}=={version}"
            else:
                line = f"{dep}  # Version not found"
        else:
            line = dep
            
        if add_comments and len(dep_to_files[dep]) <= 3:
            # Add file references for small number of files
            files = [Path(f).name for f in dep_to_files[dep]]
            line += f"  # Used in: {', '.join(files)}"
            
        lines.append(line)
    
    return '\n'.join(lines)


def create_backup_file(file_path: Path) -> Path:
    """Create a backup of an existing file"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = file_path.with_suffix(f'.{timestamp}.backup')
    
    # Ensure backup name is unique
    counter = 1
    while backup_path.exists():
        backup_path = file_path.with_suffix(f'.{timestamp}_{counter}.backup')
        counter += 1
    
    # Copy the original file
    import shutil
    shutil.copy2(file_path, backup_path)
    return backup_path


def preview_file_changes(existing_path: Path, new_content: str) -> bool:
    """Show a preview of changes and ask for confirmation"""
    try:
        with open(existing_path, 'r', encoding='utf-8') as f:
            existing_content = f.read()
    except Exception:
        existing_content = ""
    
    # Show file info
    console.print(f"\n[bold yellow]⚠️  File exists: {existing_path}[/bold yellow]")
    
    if existing_content.strip():
        console.print(f"[dim]Current file has {len(existing_content.splitlines())} lines[/dim]")
        
        # Show first few lines of existing file
        existing_lines = existing_content.strip().split('\n')
        console.print(f"\n[bold]Current content (first 5 lines):[/bold]")
        for i, line in enumerate(existing_lines[:5]):
            console.print(f"  {i+1:2d}: [dim]{line}[/dim]")
        if len(existing_lines) > 5:
            console.print(f"  ... and {len(existing_lines) - 5} more lines")
    else:
        console.print("[dim]Current file is empty[/dim]")
    
    # Show new content preview
    new_lines = new_content.strip().split('\n')
    console.print(f"\n[bold]New content (first 5 lines):[/bold]")
    for i, line in enumerate(new_lines[:5]):
        console.print(f"  {i+1:2d}: [green]{line}[/green]")
    if len(new_lines) > 5:
        console.print(f"  ... and {len(new_lines) - 5} more lines")
    
    # Ask for confirmation
    console.print(f"\n[bold red]⚠️  This will overwrite the existing file![/bold red]")
    return Confirm.ask("Do you want to proceed?", default=False)


def write_requirements_file(content: str, output_path: Optional[Path] = None,
                          project_root: Path = Path.cwd(), interactive: bool = True) -> Path:
    """Write requirements content to file with safety mechanisms"""
    if output_path is None:
        # Generate filename
        base_name = "requirements"
        suffix = ".txt"
        default_path = project_root / f"{base_name}{suffix}"
        
        # Check for existing requirements.txt
        if default_path.exists():
            if interactive:
                # Show preview and ask what to do
                console.print(f"\n[yellow]requirements.txt already exists in {project_root}[/yellow]")
                
                choices = [
                    "overwrite",
                    "backup_and_overwrite", 
                    "save_as_new",
                    "cancel"
                ]
                
                choice = Prompt.ask(
                    "What would you like to do?",
                    choices=choices,
                    default="backup_and_overwrite"
                )
                
                if choice == "cancel":
                    console.print("[red]Operation cancelled.[/red]")
                    return None
                
                elif choice == "overwrite":
                    # Show preview before overwriting
                    if not preview_file_changes(default_path, content):
                        console.print("[red]Operation cancelled.[/red]")
                        return None
                    output_path = default_path
                
                elif choice == "backup_and_overwrite":
                    # Create backup first
                    try:
                        backup_path = create_backup_file(default_path)
                        console.print(f"[green]✓[/green] Backup created: [cyan]{backup_path.name}[/cyan]")
                        output_path = default_path
                    except Exception as e:
                        console.print(f"[red]Failed to create backup: {e}[/red]")
                        return None
                
                elif choice == "save_as_new":
                    # Generate unique filename
                    counter = 1
                    while (project_root / f"{base_name}_{counter}{suffix}").exists():
                        counter += 1
                    suggested_name = f"{base_name}_{counter}{suffix}"
                    
                    custom_name = Prompt.ask(
                        "Enter filename (with .txt extension)",
                        default=suggested_name
                    )
                    
                    if not custom_name.endswith('.txt'):
                        custom_name += '.txt'
                    
                    output_path = project_root / custom_name
                    
                    # Check if the custom name also exists
                    if output_path.exists():
                        if not Confirm.ask(f"[yellow]{custom_name} also exists. Overwrite?[/yellow]", default=False):
                            console.print("[red]Operation cancelled.[/red]")
                            return None
            
            else:
                # Non-interactive mode: always use numbered filename
                counter = 1
                while (project_root / f"{base_name}_{counter}{suffix}").exists():
                    counter += 1
                output_path = project_root / f"{base_name}_{counter}{suffix}"
                console.print(f"[yellow]requirements.txt exists. Saving as {output_path.name}[/yellow]")
        
        else:
            # No existing file, use default name
            output_path = default_path
    
    else:
        # User specified output path
        if output_path.exists() and interactive:
            console.print(f"\n[yellow]File already exists: {output_path}[/yellow]")
            
            # Ask if they want to create a backup
            if Confirm.ask("Create backup before overwriting?", default=True):
                try:
                    backup_path = create_backup_file(output_path)
                    console.print(f"[green]✓[/green] Backup created: [cyan]{backup_path.name}[/cyan]")
                except Exception as e:
                    console.print(f"[red]Failed to create backup: {e}[/red]")
                    if not Confirm.ask("Continue without backup?", default=False):
                        console.print("[red]Operation cancelled.[/red]")
                        return None
            
            # Show preview
            if not preview_file_changes(output_path, content):
                console.print("[red]Operation cancelled.[/red]")
                return None
    
    # Final safety check
    if output_path is None:
        console.print("[red]No output path determined. Operation cancelled.[/red]")
        return None
    
    # Write file
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return output_path
    except Exception as e:
        console.print(f"[red]Failed to write file: {e}[/red]")
        return None


def build_package_dependency_tree(packages: Set[str], max_depth: int = 2) -> Dict[str, Dict]:
    """Build a dependency tree for external packages"""
    package_tree = {}
    seen = set()
    
    def process_package(pkg_name: str, depth: int = 0) -> Dict:
        if depth > max_depth or pkg_name in seen:
            return {}
            
        seen.add(pkg_name)
        info = get_package_info(pkg_name)
        
        pkg_data = {
            'version': info.get('version'),
            'summary': info.get('summary', 'No description available'),
            'dependencies': {},
            'depth': depth
        }
        
        # Process dependencies
        for req in info.get('requires', []):
            # Extract package name from requirement (handle version specs)
            dep_name = req.split()[0] if req else ''
            dep_name = dep_name.split('=')[0].split('<')[0].split('>')[0].split('!')[0].split('~')[0]
            
            if dep_name and dep_name != pkg_name:  # Avoid self-dependencies
                pkg_data['dependencies'][dep_name] = process_package(dep_name, depth + 1)
        
        return pkg_data
    
    for package in packages:
        package_tree[package] = process_package(package)
    
    return package_tree


def display_package_dependency_tree(package_tree: Dict[str, Dict], console: Console):
    """Display package dependency tree in johnnydep style"""
    console.print("\n[bold]Package Dependency Analysis:[/bold]")
    
    # Create a summary table first
    summary_table = Table(show_header=True, header_style="bold cyan", box=None)
    summary_table.add_column("Package", style="cyan")
    summary_table.add_column("Summary", style="dim", max_width=80)
    
    def collect_all_packages(tree: Dict, packages: Dict):
        for pkg_name, pkg_data in tree.items():
            if pkg_name not in packages:
                version = pkg_data.get('version', 'unknown')
                summary = pkg_data.get('summary', 'No description available') or 'No description available'
                packages[pkg_name] = {'version': version, 'summary': summary}
            
            # Recursively collect dependencies
            if 'dependencies' in pkg_data:
                collect_all_packages(pkg_data['dependencies'], packages)
    
    all_packages = {}
    collect_all_packages(package_tree, all_packages)
    
    # Build Rich tree structure
    from rich.tree import Tree as RichTree
    
    tree = RichTree("📦 [bold]Dependencies[/bold]")
    
    def add_tree_node(parent_tree, pkg_tree: Dict, prefix: str = ""):
        for pkg_name, pkg_data in pkg_tree.items():
            version = pkg_data.get('version', 'unknown')
            summary = pkg_data.get('summary', 'No description available') or 'No description available'
            
            # Truncate long summaries
            if len(summary) > 70:
                summary = summary[:67] + "..."
            
            # Create node label
            if version and version != 'unknown':
                label = f"[cyan]{pkg_name}[/cyan] [dim]({version})[/dim]"
            else:
                label = f"[cyan]{pkg_name}[/cyan] [red](not installed)[/red]"
            
            node = parent_tree.add(label)
            
            # Add summary as a sub-item
            if summary and summary != 'No description available':
                node.add(f"[dim]{summary}[/dim]")
            
            # Add dependencies
            if pkg_data.get('dependencies'):
                add_tree_node(node, pkg_data['dependencies'], prefix + "  ")
    
    add_tree_node(tree, package_tree)
    console.print(tree)
    
    # Also show the table summary
    console.print(f"\n[bold]Package Summary:[/bold]")
    for pkg_name in sorted(all_packages.keys()):
        pkg_info = all_packages[pkg_name]
        version = pkg_info['version']
        summary = pkg_info['summary']
        
        if len(summary) > 80:
            summary = summary[:77] + "..."
            
        version_str = version if version and version != 'unknown' else '[red]not installed[/red]'
        summary_table.add_row(f"{pkg_name} ({version_str})", summary)
    
    console.print(summary_table)


def build_dependency_tree(file_path: Path, project_root: Path, depth: int, 
                         check_lint: bool = True, search_pattern: Optional[str] = None,
                         search_type: str = 'text', check_git: bool = True,
                         show_metrics: bool = True) -> Tuple[Tree, Dict[str, FileInfo], int]:
    """Build a dependency tree for a Python file"""
    seen = set()
    file_stats = {}
    total_files = 0
    
    # Analyze root file
    root_info = analyze_file(file_path, project_root, search_pattern, search_type, check_git)
    file_stats[str(file_path)] = root_info
    
    root_label = format_file_label(root_info, project_root, show_metrics)
    tree = Tree(root_label)
    seen.add(file_path.resolve())
    total_files = 1
    
    def add_dependencies(parent_tree: Tree, current_file: Path, current_depth: int):
        nonlocal total_files
        
        if current_depth >= depth:
            return
            
        imports = extract_imports(current_file)
        
        for import_name in sorted(imports):
            import_parts = import_name.split('.')
            
            # Try to find the imported module in the project
            for i in range(len(import_parts), 0, -1):
                potential_path = project_root / Path(*import_parts[:i]).with_suffix('.py')
                
                if potential_path.exists() and potential_path.resolve() not in seen:
                    seen.add(potential_path.resolve())
                    
                    # Analyze the file
                    with Progress(
                        SpinnerColumn(),
                        TextColumn("[progress.description]{task.description}"),
                        transient=True,
                    ) as progress:
                        task = progress.add_task(f"Analyzing {potential_path.name}...", total=1)
                        file_info = analyze_file(potential_path, project_root, 
                                               search_pattern, search_type, check_git)
                        progress.advance(task)
                    
                    file_stats[str(potential_path)] = file_info
                    total_files += 1
                    
                    # Add to tree
                    label = format_file_label(file_info, project_root, show_metrics)
                    child_tree = parent_tree.add(label)
                    
                    # Add TODOs if present and no search
                    if file_info.todos and not search_pattern:
                        for line_no, todo_text in file_info.todos[:3]:  # Show max 3 TODOs
                            todo_label = Text()
                            todo_label.append("  └─ ", style="dim")
                            todo_label.append(f"{todo_text} ", style="bright_blue")
                            todo_label.append(f"(line {line_no})", style="dim")
                            child_tree.add(todo_label)
                            
                    # Add search matches if present
                    if file_info.search_matches:
                        for line_no, match_text in file_info.search_matches[:3]:  # Show max 3 matches
                            match_label = Text()
                            match_label.append("  └─ ", style="dim")
                            match_label.append(f"Line {line_no}: ", style="magenta")
                            match_label.append(match_text[:80], style="bright_magenta")
                            if len(match_text) > 80:
                                match_label.append("...", style="dim")
                            child_tree.add(match_label)
                    
                    # Recursively add dependencies
                    add_dependencies(child_tree, potential_path, current_depth + 1)
                    break
                    
                # Also check for package __init__.py
                potential_package = project_root / Path(*import_parts[:i]) / '__init__.py'
                
                if potential_package.exists() and potential_package.resolve() not in seen:
                    # Add all Python files in the package
                    package_dir = potential_package.parent
                    python_files = get_python_files_in_directory(package_dir, seen)
                    
                    for py_file in python_files:
                        with Progress(
                            SpinnerColumn(),
                            TextColumn("[progress.description]{task.description}"),
                            transient=True,
                        ) as progress:
                            task = progress.add_task(f"Analyzing {py_file.name}...", total=1)
                            file_info = analyze_file(py_file, project_root,
                                                   search_pattern, search_type, check_git)
                            progress.advance(task)
                        
                        file_stats[str(py_file)] = file_info
                        total_files += 1
                        
                        label = format_file_label(file_info, project_root, show_metrics)
                        child_tree = parent_tree.add(label)
                        add_dependencies(child_tree, py_file, current_depth + 1)
                    break
    
    add_dependencies(tree, file_path, 0)
    return tree, file_stats, total_files


def display_summary_table(file_stats: Dict[str, FileInfo], show_search: bool = False):
    """Display a summary table of file statistics"""
    # Group by file type
    type_stats = {}
    
    for file_info in file_stats.values():
        if file_info.file_type not in type_stats:
            type_stats[file_info.file_type] = {
                'count': 0,
                'total_lines': 0,
                'total_complexity': 0,
                'total_functions': 0,
                'total_classes': 0,
                'errors': 0,
                'warnings': 0,
                'todos': 0,
                'search_matches': 0
            }
        
        stats = type_stats[file_info.file_type]
        stats['count'] += 1
        stats['total_lines'] += file_info.lines
        stats['total_complexity'] += file_info.complexity
        stats['total_functions'] += file_info.functions
        stats['total_classes'] += file_info.classes
        stats['errors'] += file_info.lint_errors
        stats['warnings'] += file_info.lint_warnings
        stats['todos'] += len(file_info.todos)
        stats['search_matches'] += len(file_info.search_matches)
    
    # Create table
    table = Table(title="File Statistics Summary", show_header=True, header_style="bold cyan")
    table.add_column("Type", style="cyan")
    table.add_column("Count", justify="right")
    table.add_column("Total Lines", justify="right")
    table.add_column("Avg Lines", justify="right")
    table.add_column("Functions", justify="right")
    table.add_column("Classes", justify="right")
    table.add_column("Avg Complexity", justify="right")
    table.add_column("TODOs", justify="right", style="bright_blue")
    table.add_column("Errors", justify="right", style="red")
    table.add_column("Warnings", justify="right", style="yellow")
    
    if show_search:
        table.add_column("Matches", justify="right", style="magenta")
    
    # Sort by type
    type_order = ['main', 'model', 'service', 'utils', 'test', 'other']
    
    # Add rows
    total_stats = {
        'count': 0,
        'total_lines': 0,
        'total_complexity': 0,
        'total_functions': 0,
        'total_classes': 0,
        'errors': 0,
        'warnings': 0,
        'todos': 0,
        'search_matches': 0
    }
    
    for file_type in type_order:
        if file_type in type_stats:
            stats = type_stats[file_type]
            avg_lines = stats['total_lines'] // stats['count'] if stats['count'] > 0 else 0
            avg_complexity = stats['total_complexity'] / stats['count'] if stats['count'] > 0 else 0
            
            icon = get_file_type_icon(file_type)
            
            row = [
                f"{icon} {file_type}",
                str(stats['count']),
                str(stats['total_lines']),
                str(avg_lines),
                str(stats['total_functions']),
                str(stats['total_classes']),
                f"{avg_complexity:.1f}",
                str(stats['todos']) if stats['todos'] > 0 else "-",
                str(stats['errors']) if stats['errors'] > 0 else "-",
                str(stats['warnings']) if stats['warnings'] > 0 else "-"
            ]
            
            if show_search:
                row.append(str(stats['search_matches']) if stats['search_matches'] > 0 else "-")
            
            table.add_row(*row)
            
            # Update totals
            for key in total_stats:
                total_stats[key] += stats[key]
    
    # Add total row
    if type_stats:
        avg_lines = total_stats['total_lines'] // total_stats['count'] if total_stats['count'] > 0 else 0
        avg_complexity = total_stats['total_complexity'] / total_stats['count'] if total_stats['count'] > 0 else 0
        
        table.add_section()
        row = [
            "Total",
            str(total_stats['count']),
            str(total_stats['total_lines']),
            str(avg_lines),
            str(total_stats['total_functions']),
            str(total_stats['total_classes']),
            f"{avg_complexity:.1f}",
            str(total_stats['todos']) if total_stats['todos'] > 0 else "-",
            str(total_stats['errors']) if total_stats['errors'] > 0 else "-",
            str(total_stats['warnings']) if total_stats['warnings'] > 0 else "-"
        ]
        
        if show_search:
            row.append(str(total_stats['search_matches']) if total_stats['search_matches'] > 0 else "-")
        
        table.add_row(*row, style="bold")
    
    console.print(table)


def display_lint_summary(file_stats: Dict[str, FileInfo]):
    """Display summary of lint issues"""
    files_with_errors = []
    files_with_warnings = []
    
    for file_path, file_info in file_stats.items():
        if file_info.lint_errors > 0:
            files_with_errors.append((file_info.path, file_info.lint_errors))
        if file_info.lint_warnings > 0:
            files_with_warnings.append((file_info.path, file_info.lint_warnings))
    
    if files_with_errors or files_with_warnings:
        console.print("\n[bold]Lint Issues:[/bold]")
        
        if files_with_errors:
            console.print("\n[red]Files with errors:[/red]")
            for file_path, count in sorted(files_with_errors, key=lambda x: x[1], reverse=True)[:10]:
                console.print(f"  • {file_path.name} - {count} error{'s' if count > 1 else ''}")
        
        if files_with_warnings:
            console.print("\n[yellow]Files with warnings:[/yellow]")
            for file_path, count in sorted(files_with_warnings, key=lambda x: x[1], reverse=True)[:10]:
                console.print(f"  • {file_path.name} - {count} warning{'s' if count > 1 else ''}")


def display_todos_summary(file_stats: Dict[str, FileInfo]):
    """Display summary of TODO comments"""
    all_todos = []
    
    for file_path, file_info in file_stats.items():
        for line_no, todo_text in file_info.todos:
            all_todos.append((file_info.path, line_no, todo_text))
    
    if all_todos:
        console.print("\n[bold bright_blue]TODO/FIXME Comments:[/bold bright_blue]")
        
        # Group by type
        todo_types = {}
        for file_path, line_no, todo_text in all_todos:
            todo_type = todo_text.split(':')[0]
            if todo_type not in todo_types:
                todo_types[todo_type] = []
            todo_types[todo_type].append((file_path, line_no, todo_text))
        
        # Display by type
        for todo_type in sorted(todo_types.keys()):
            todos = todo_types[todo_type]
            console.print(f"\n[bright_blue]{todo_type}s ({len(todos)}):[/bright_blue]")
            
            for file_path, line_no, todo_text in todos[:5]:  # Show max 5 per type
                console.print(f"  • {file_path.name}:{line_no} - {todo_text}")
            
            if len(todos) > 5:
                console.print(f"  ... and {len(todos) - 5} more")


@click.command()
@click.argument('file_path', type=click.Path(exists=True, path_type=Path))
@click.option('-d', '--depth', default=2, help='Maximum depth to traverse')
@click.option('-r', '--project-root', type=click.Path(exists=True, path_type=Path), 
              help='Project root directory (defaults to file\'s parent)')
@click.option('-c', '--show-code', is_flag=True, help='Display import statements')
@click.option('-l', '--check-lint/--no-check-lint', default=True, 
              help='Enable/disable lint checking')
@click.option('-s', '--show-stats/--no-show-stats', default=True, 
              help='Show/hide statistics table')
@click.option('--search', '-S', help='Search for text/pattern in files')
@click.option('--search-type', type=click.Choice(['text', 'class', 'function', 'import']), 
              default='text', help='Type of search to perform')
@click.option('--show-todos/--no-show-todos', default=True,
              help='Show/hide TODO comments')
@click.option('--check-git/--no-check-git', default=True,
              help='Show/hide git status')
@click.option('--show-metrics/--no-show-metrics', default=True,
              help='Show/hide inline metrics (size, complexity, etc.)')
@click.option('--generate-requirements', '-R', is_flag=True,
              help='Generate requirements.txt from detected dependencies')
@click.option('--requirements-output', '-o', type=click.Path(path_type=Path),
              help='Output path for requirements.txt (default: auto-generated)')
@click.option('--no-versions', is_flag=True,
              help='Generate requirements.txt without version numbers')
@click.option('--no-interactive', is_flag=True,
              help='Don\'t prompt for confirmation when requirements.txt exists')
@click.option('--analyze-deps', is_flag=True,
              help='Show detailed dependency analysis like johnnydep')
@click.option('--dep-depth', default=2, type=int,
              help='Maximum depth for dependency analysis (default: 2)')
def cli(file_path: Path, depth: int, project_root: Optional[Path], show_code: bool, 
        check_lint: bool, show_stats: bool, search: Optional[str], search_type: str,
        show_todos: bool, check_git: bool, show_metrics: bool,
        generate_requirements: bool, requirements_output: Optional[Path], no_versions: bool,
        no_interactive: bool, analyze_deps: bool, dep_depth: int):
    """Advanced Python Dependency Tree Analyzer with search, complexity, and more"""
    
    # Set project root
    if project_root is None:
        project_root = file_path.parent
    
    # Display header
    header = Panel(
        f"[bold]Advanced Python Dependency Analyzer[/bold]\n\n"
        f"File: [cyan]{file_path}[/cyan]\n"
        f"Project root: [green]{project_root}[/green]\n"
        f"Max depth: [yellow]{depth}[/yellow]\n"
        f"Lint checking: [{'green' if check_lint else 'red'}]{'enabled' if check_lint else 'disabled'}[/]\n"
        f"Git status: [{'green' if check_git else 'red'}]{'enabled' if check_git else 'disabled'}[/]" +
        (f"\nSearch: [magenta]{search}[/magenta] (type: {search_type})" if search else ""),
        title="Analysis Settings",
        border_style="blue"
    )
    console.print(header)
    
    # Display legend
    legend_items = [
        "📊 Models", "🌐 Services", "🔧 Utils", "🧪 Tests", "🚀 Main"
    ]
    
    if show_metrics:
        legend_items.extend([
            "Size", "Lines", "Imports↓", "C:Complexity",
            "[Nc/Nf]", "E:Errors", "W:Warnings", "📌TODOs"
        ])
        
    if check_git:
        legend_items.append("[M]:Modified")
        
    if search:
        legend_items.append("🔍:Matches")
    
    console.print("\n[bold]Legend:[/bold]")
    console.print(" | ".join(legend_items))
    
    # Build dependency tree
    start_time = time.time()
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True
    ) as progress:
        task = progress.add_task("Building dependency tree...", total=None)
        tree, file_stats, total_files = build_dependency_tree(
            file_path, project_root, depth, check_lint, 
            search, search_type, check_git, show_metrics
        )
        progress.update(task, completed=True)
    
    # Display tree
    console.print("\n", Panel(tree, title="Dependency Tree", border_style="green"))
    
    # Display summary
    elapsed_time = time.time() - start_time
    console.print(f"\nFound [cyan]{total_files}[/cyan] files with "
                 f"[green]{sum(f.imports for f in file_stats.values())}[/green] total dependencies "
                 f"in [yellow]{elapsed_time:.2f}s[/yellow]")
    
    # Display statistics table
    if show_stats:
        console.print()
        display_summary_table(file_stats, show_search=bool(search))
    
    # Display lint summary
    if check_lint:
        display_lint_summary(file_stats)
    
    # Display TODOs summary
    if show_todos and not search:
        display_todos_summary(file_stats)
    
    # Display search results summary
    if search:
        total_matches = sum(len(f.search_matches) for f in file_stats.values())
        if total_matches > 0:
            console.print(f"\n[bold magenta]Search Results:[/bold magenta] Found {total_matches} matches for '{search}'")
        else:
            console.print(f"\n[bold red]No matches found for '{search}'[/bold red]")
    
    # Display import statements if requested
    if show_code:
        console.print("\n[bold]Import Statements:[/bold]")
        for file_path_str, file_info in list(file_stats.items())[:10]:
            if file_info.imports > 0:
                console.print(f"\n[cyan]{file_info.path.name}:[/cyan]")
                try:
                    with open(file_info.path, 'r') as f:
                        lines = f.readlines()
                        for i, line in enumerate(lines):
                            if line.strip().startswith(('import ', 'from ')):
                                syntax = Syntax(line.strip(), "python", theme="monokai", line_numbers=False)
                                console.print(f"  ", syntax, end="")
                except Exception:
                    console.print("  [red]Error reading file[/red]")
    
    # Generate requirements.txt if requested
    if generate_requirements:
        console.print("\n[bold]Generating Requirements File...[/bold]")
        
        # Extract external dependencies
        external_deps = extract_external_dependencies(file_stats, project_root)
        
        if external_deps:
            # Display found dependencies
            all_deps = set()
            for deps in external_deps.values():
                all_deps.update(deps)
            
            console.print(f"\nFound [cyan]{len(all_deps)}[/cyan] external dependencies:")
            
            # Show enhanced dependency analysis if requested
            if analyze_deps:
                console.print("\n[bold]Building dependency tree...[/bold]")
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    console=console,
                    transient=True
                ) as progress:
                    task = progress.add_task("Analyzing package dependencies...", total=None)
                    
                    # Build package dependency tree
                    package_tree = build_package_dependency_tree(all_deps, dep_depth)
                    
                    progress.update(task, completed=True)
                
                # Display the dependency tree
                display_package_dependency_tree(package_tree, console)
            else:
                # Show simple table
                deps_table = Table(show_header=True, header_style="bold cyan")
                deps_table.add_column("Package", style="cyan")
                deps_table.add_column("Version", style="green")
                deps_table.add_column("Used In", style="dim")
                
                dep_to_files = {}
                for file_path, deps in external_deps.items():
                    for dep in deps:
                        if dep not in dep_to_files:
                            dep_to_files[dep] = []
                        dep_to_files[dep].append(Path(file_path).name)
                
                for dep in sorted(all_deps):
                    version = get_installed_package_version(dep) if not no_versions else "N/A"
                    files = dep_to_files[dep]
                    files_str = ", ".join(files[:3])
                    if len(files) > 3:
                        files_str += f" (+{len(files)-3} more)"
                    
                    deps_table.add_row(dep, version or "Not found", files_str)
                
                console.print(deps_table)
            
            # Generate content
            content = generate_requirements_content(
                external_deps, 
                include_versions=not no_versions,
                add_comments=True
            )
            
            # Write file
            output_file = write_requirements_file(content, requirements_output, project_root, not no_interactive)
            
            console.print(f"\n[green]✓[/green] Requirements file written to: [cyan]{output_file}[/cyan]")
            
            # Show preview
            console.print("\n[bold]Preview:[/bold]")
            preview_lines = content.split('\n')[:10]
            for line in preview_lines:
                console.print(f"  {line}")
            if len(content.split('\n')) > 10:
                console.print(f"  ... and {len(content.split('\n')) - 10} more lines")
        else:
            console.print("\n[yellow]No external dependencies found.[/yellow]")
            console.print("All imports appear to be from the standard library or internal modules.")


if __name__ == '__main__':
    cli()