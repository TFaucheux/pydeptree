import pytest
from pathlib import Path
from click.testing import CliRunner
from pydeptree.cli import main, parse_imports, is_project_module


class TestCLI:
    def test_help(self):
        runner = CliRunner()
        result = runner.invoke(main, ['--help'])
        assert result.exit_code == 0
        assert 'Analyze Python file dependencies' in result.output
    
    def test_non_python_file(self, tmp_path):
        non_py_file = tmp_path / "test.txt"
        non_py_file.write_text("not python")
        
        runner = CliRunner()
        result = runner.invoke(main, [str(non_py_file)])
        assert result.exit_code == 1
        assert 'must be a Python file' in result.output
    
    def test_basic_analysis(self, tmp_path):
        # Create test files
        main_file = tmp_path / "main.py"
        main_file.write_text("import helper\nhelper.do_something()")
        
        helper_file = tmp_path / "helper.py"
        helper_file.write_text("def do_something():\n    pass")
        
        runner = CliRunner()
        result = runner.invoke(main, [str(main_file)])
        assert result.exit_code == 0
        assert 'main.py' in result.output
        assert 'helper.py' in result.output


class TestImportParsing:
    def test_parse_imports(self, tmp_path):
        test_file = tmp_path / "test.py"
        test_file.write_text("""
import os
import sys
from pathlib import Path
from collections import defaultdict
import local_module
        """)
        
        imports = parse_imports(test_file, tmp_path)
        assert 'os' in imports
        assert 'sys' in imports
        assert 'pathlib' in imports
        assert 'collections' in imports
        assert 'local_module' in imports
    
    def test_is_project_module(self, tmp_path):
        # Create a local module
        local_module = tmp_path / "my_module.py"
        local_module.write_text("# module")
        
        # Create a package
        package_dir = tmp_path / "my_package"
        package_dir.mkdir()
        (package_dir / "__init__.py").write_text("")
        
        assert is_project_module("my_module", tmp_path) == True
        assert is_project_module("my_package", tmp_path) == True
        assert is_project_module("os", tmp_path) == False
        assert is_project_module("sys", tmp_path) == False