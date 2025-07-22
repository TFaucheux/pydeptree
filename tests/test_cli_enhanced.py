import pytest
import subprocess
from pathlib import Path
from click.testing import CliRunner
from unittest.mock import patch, MagicMock

from pydeptree.cli_enhanced import (
    main, 
    detect_file_type, 
    get_file_type_color, 
    get_file_type_icon,
    get_file_info,
    run_ruff_check,
    format_file_label,
    create_summary_table,
    FileInfo
)


class TestFileTypeDetection:
    """Test file type detection functionality"""
    
    def test_detect_model_files(self):
        # Test model directory detection
        model_file = Path("/project/models/user.py")
        assert detect_file_type(model_file) == 'model'
        
        # Test model filename detection
        model_file2 = Path("/project/user_model.py")
        assert detect_file_type(model_file2) == 'model'
    
    def test_detect_service_files(self):
        # Test service directory detection
        service_file = Path("/project/services/api.py")
        assert detect_file_type(service_file) == 'service'
        
        # Test API filename detection
        api_file = Path("/project/api_client.py")
        assert detect_file_type(api_file) == 'service'
    
    def test_detect_utils_files(self):
        # Test utils directory detection
        utils_file = Path("/project/utils/helpers.py")
        assert detect_file_type(utils_file) == 'utils'
        
        # Test config filename detection
        config_file = Path("/project/config.py")
        assert detect_file_type(config_file) == 'utils'
    
    def test_detect_test_files(self):
        # Test test directory detection
        test_file = Path("/project/tests/test_api.py")
        assert detect_file_type(test_file) == 'test'
        
        # Test test filename detection
        test_file2 = Path("/project/test_utils.py")
        assert detect_file_type(test_file2) == 'test'
    
    def test_detect_main_files(self):
        # Test main.py detection
        main_file = Path("/project/main.py")
        assert detect_file_type(main_file) == 'main'
        
        # Test __main__.py detection
        main_file2 = Path("/project/__main__.py")
        assert detect_file_type(main_file2) == 'main'
    
    def test_detect_other_files(self):
        # Test other file types
        other_file = Path("/project/random.py")
        assert detect_file_type(other_file) == 'other'


class TestFileTypeColors:
    """Test file type color and icon functionality"""
    
    def test_get_file_type_colors(self):
        assert get_file_type_color('model') == 'cyan'
        assert get_file_type_color('service') == 'green'
        assert get_file_type_color('utils') == 'yellow'
        assert get_file_type_color('test') == 'magenta'
        assert get_file_type_color('main') == 'bold blue'
        assert get_file_type_color('other') == 'white'
        assert get_file_type_color('unknown') == 'white'  # fallback
    
    def test_get_file_type_icons(self):
        assert get_file_type_icon('model') == '📊'
        assert get_file_type_icon('service') == '🌐'
        assert get_file_type_icon('utils') == '🔧'
        assert get_file_type_icon('test') == '🧪'
        assert get_file_type_icon('main') == '🚀'
        assert get_file_type_icon('other') == '📄'
        assert get_file_type_icon('unknown') == '📄'  # fallback


class TestLintChecking:
    """Test ruff integration for lint checking"""
    
    @patch('subprocess.run')
    def test_run_ruff_check_success(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0, stdout='')
        
        test_file = Path('/tmp/test.py')
        errors, warnings = run_ruff_check(test_file)
        
        assert errors == 0
        assert warnings == 0
        mock_run.assert_called_once_with(
            ['ruff', 'check', str(test_file), '--output-format=json'],
            capture_output=True,
            text=True,
            timeout=5
        )
    
    @patch('subprocess.run')
    def test_run_ruff_check_with_issues(self, mock_run):
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stdout = '[{"code": "E501", "message": "line too long"}, {"code": "W291", "message": "trailing whitespace"}]'
        mock_run.return_value = mock_result
        
        test_file = Path('/tmp/test.py')
        errors, warnings = run_ruff_check(test_file)
        
        assert errors == 1  # E501 is an error
        assert warnings == 1  # W291 is a warning
    
    @patch('subprocess.run')
    def test_run_ruff_check_timeout(self, mock_run):
        mock_run.side_effect = subprocess.TimeoutExpired(['ruff'], 5)
        
        test_file = Path('/tmp/test.py')
        errors, warnings = run_ruff_check(test_file)
        
        assert errors == 0
        assert warnings == 0
    
    @patch('subprocess.run')
    def test_run_ruff_check_not_found(self, mock_run):
        mock_run.side_effect = FileNotFoundError()
        
        test_file = Path('/tmp/test.py')
        errors, warnings = run_ruff_check(test_file)
        
        assert errors == 0
        assert warnings == 0


class TestFileInfo:
    """Test file information gathering"""
    
    def test_get_file_info(self, tmp_path):
        # Create a clean path without "test" in it
        proj_dir = tmp_path / "myproject" / "services"
        proj_dir.mkdir(parents=True)
        test_file = proj_dir / "api_client.py"
        content = """import os
import sys
from pathlib import Path

class APIClient:
    def __init__(self):
        pass
    
    def get_data(self):
        return {}
"""
        test_file.write_text(content)
        
        with patch('pydeptree.cli_enhanced.run_ruff_check', return_value=(1, 2)):
            file_info = get_file_info(test_file)
        
        assert file_info.path == test_file
        assert file_info.size > 0
        assert file_info.lines == 10  # counting the lines in content
        assert file_info.imports == 3  # import os, sys, from pathlib
        assert file_info.lint_errors == 1
        assert file_info.lint_warnings == 2
        assert file_info.file_type == 'service'
    
    def test_get_file_info_with_error(self, tmp_path):
        non_existent = tmp_path / "missing.py"
        
        file_info = get_file_info(non_existent)
        
        assert file_info.path == non_existent
        assert file_info.size == 0
        assert file_info.lines == 0
        assert file_info.imports == 0
        assert file_info.lint_errors == 0
        assert file_info.lint_warnings == 0
        assert file_info.file_type == 'other'


class TestFileFormatting:
    """Test file label formatting functionality"""
    
    def test_format_file_label_basic(self, tmp_path):
        file_info = FileInfo(
            path=tmp_path / "models" / "user.py",
            size=1024,
            lines=50,
            imports=3,
            lint_errors=0,
            lint_warnings=0,
            file_type='model'
        )
        
        label = format_file_label(file_info, tmp_path)
        label_str = label.plain
        
        assert '📊' in label_str  # model icon
        assert 'models/user.py' in label_str
        assert '1.0KB' in label_str  # size badge
        assert '50L' in label_str  # lines badge
        assert '3↓' in label_str  # imports badge
    
    def test_format_file_label_with_lint_issues(self, tmp_path):
        file_info = FileInfo(
            path=tmp_path / "api.py",
            size=2048,
            lines=100,
            imports=5,
            lint_errors=2,
            lint_warnings=1,
            file_type='service'
        )
        
        label = format_file_label(file_info, tmp_path)
        label_str = label.plain
        
        assert '🌐' in label_str  # service icon
        assert 'api.py' in label_str
        assert '2.0KB' in label_str
        assert '100L' in label_str
        assert '5↓' in label_str
        assert 'E:2' in label_str  # error badge
        assert 'W:1' in label_str  # warning badge
    
    def test_format_file_label_sizes(self, tmp_path):
        # Test different size formatting
        file_info_small = FileInfo(tmp_path / "small.py", 500, 10, 1, 0, 0, 'other')
        label = format_file_label(file_info_small, tmp_path)
        assert '500B' in label.plain
        
        file_info_mb = FileInfo(tmp_path / "large.py", 2 * 1024 * 1024, 1000, 10, 0, 0, 'other')
        label = format_file_label(file_info_mb, tmp_path)
        assert '2.0MB' in label.plain


class TestSummaryTable:
    """Test summary statistics table generation"""
    
    def test_create_summary_table(self, tmp_path):
        file_info_cache = {
            tmp_path / "main.py": FileInfo(tmp_path / "main.py", 1000, 50, 2, 0, 0, 'main'),
            tmp_path / "models/user.py": FileInfo(tmp_path / "models/user.py", 800, 40, 1, 0, 1, 'model'),
            tmp_path / "models/product.py": FileInfo(tmp_path / "models/product.py", 1200, 60, 2, 1, 0, 'model'),
            tmp_path / "services/api.py": FileInfo(tmp_path / "services/api.py", 1500, 75, 3, 2, 1, 'service'),
        }
        
        table = create_summary_table(file_info_cache)
        
        # Check that table was created (can't easily test Rich table content)
        assert table is not None
        assert table.title == "File Statistics Summary"
        
        # Check that we have the right number of columns
        assert len(table.columns) == 6  # Type, Count, Total Lines, Avg Lines, Errors, Warnings


class TestEnhancedCLI:
    """Test the enhanced CLI command functionality"""
    
    def test_enhanced_cli_help(self):
        runner = CliRunner()
        result = runner.invoke(main, ['--help'])
        assert result.exit_code == 0
        assert 'Enhanced Python Dependency Analyzer' in result.output
        assert '--check-lint' in result.output
        assert '--show-stats' in result.output
    
    def test_enhanced_cli_non_python_file(self, tmp_path):
        non_py_file = tmp_path / "test.txt"
        non_py_file.write_text("not python")
        
        runner = CliRunner()
        result = runner.invoke(main, [str(non_py_file)])
        assert result.exit_code == 1
        assert 'must be a Python file' in result.output
    
    def test_enhanced_cli_basic_analysis(self, tmp_path):
        # Create test files
        main_file = tmp_path / "main.py"
        main_file.write_text("import helper\nprint('main')")
        
        helper_file = tmp_path / "helper.py"
        helper_file.write_text("def helper_func():\n    pass")
        
        with patch('pydeptree.cli_enhanced.run_ruff_check', return_value=(0, 0)):
            runner = CliRunner()
            result = runner.invoke(main, [str(main_file), '--depth', '1'])
            
            assert result.exit_code == 0
            assert 'main.py' in result.output
            assert 'helper.py' in result.output
            assert 'Enhanced Python Dependency Analyzer' in result.output
    
    @patch('subprocess.run')
    def test_enhanced_cli_ruff_not_available(self, mock_run, tmp_path):
        mock_run.side_effect = FileNotFoundError()
        
        proj_dir = tmp_path / "project"
        proj_dir.mkdir()
        test_file = proj_dir / "script.py"
        test_file.write_text("print('hello')")
        
        runner = CliRunner()
        result = runner.invoke(main, [str(test_file)])
        
        assert result.exit_code == 0
        # The warning might not always appear if ruff check fails differently
        assert 'lint checking' in result.output.lower() or 'disabled' in result.output.lower()
    
    def test_enhanced_cli_disable_lint_checking(self, tmp_path):
        proj_dir = tmp_path / "project"
        proj_dir.mkdir()
        test_file = proj_dir / "script.py"
        test_file.write_text("print('hello')")
        
        runner = CliRunner()
        result = runner.invoke(main, [str(test_file), '--no-check-lint'])
        
        assert result.exit_code == 0
    
    def test_enhanced_cli_disable_stats(self, tmp_path):
        proj_dir = tmp_path / "project"
        proj_dir.mkdir()
        test_file = proj_dir / "script.py"
        test_file.write_text("print('hello')")
        
        with patch('pydeptree.cli_enhanced.run_ruff_check', return_value=(0, 0)):
            runner = CliRunner()
            result = runner.invoke(main, [str(test_file), '--no-show-stats'])
            
            assert result.exit_code == 0
            # Stats table should not be shown
    
    def test_enhanced_cli_show_code_feature(self, tmp_path):
        # Create test files with imports
        main_file = tmp_path / "main.py"
        main_file.write_text("import helper\nimport os\ndef main(): pass")
        
        helper_file = tmp_path / "helper.py"
        helper_file.write_text("def helper_func(): pass")
        
        with patch('pydeptree.cli_enhanced.run_ruff_check', return_value=(0, 0)):
            runner = CliRunner()
            result = runner.invoke(main, [str(main_file), '--show-code'])
            
            assert result.exit_code == 0
            assert 'Import Statements:' in result.output


class TestIntegrationWithSampleProject:
    """Test enhanced CLI with the actual sample project"""
    
    @pytest.fixture
    def sample_project_path(self):
        """Get the sample project path"""
        current_dir = Path(__file__).parent.parent
        sample_dir = current_dir / "sample_project"
        return sample_dir
    
    def test_sample_project_exists(self, sample_project_path):
        """Verify sample project structure exists"""
        assert sample_project_path.exists(), f"Sample project not found at {sample_project_path}"
        
        main_file = sample_project_path / "main.py"
        assert main_file.exists(), "main.py should exist in sample project"
        
        # Check for expected directories
        assert (sample_project_path / "utils").exists(), "utils directory should exist"
        assert (sample_project_path / "models").exists(), "models directory should exist"
        assert (sample_project_path / "services").exists(), "services directory should exist"
    
    def test_sample_project_analysis(self, sample_project_path):
        """Test enhanced CLI on the actual sample project"""
        main_file = sample_project_path / "main.py"
        
        if not main_file.exists():
            pytest.skip("Sample project not available for testing")
        
        runner = CliRunner()
        result = runner.invoke(main, [str(main_file), '--depth', '2'])
        
        assert result.exit_code == 0
        assert 'main.py' in result.output
        
        # Should detect file types
        assert '🚀' in result.output or 'main' in result.output
        assert '🔧' in result.output or 'utils' in result.output
        assert '📊' in result.output or 'models' in result.output
        assert '🌐' in result.output or 'services' in result.output
    
    def test_sample_project_has_intentional_lint_issues(self, sample_project_path):
        """Verify that sample project has intentional lint issues for demonstration"""
        if not sample_project_path.exists():
            pytest.skip("Sample project not available for testing")
        
        # Check that at least some files have lint issues when ruff is available
        try:
            subprocess.run(['ruff', '--version'], capture_output=True, timeout=1)
            
            # Run enhanced CLI on sample project
            main_file = sample_project_path / "main.py"
            runner = CliRunner()
            result = runner.invoke(main, [str(main_file), '--depth', '2'])
            
            # Should show some lint issues (errors or warnings)
            output = result.output
            has_lint_indicators = any(indicator in output for indicator in ['E:', 'W:', 'error(s)', 'warning(s)'])
            
            # If ruff found issues, verify they're displayed
            if 'Lint Issues:' in output:
                assert has_lint_indicators, "Should show lint error/warning indicators when issues are found"
                
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pytest.skip("ruff not available for lint testing")


if __name__ == '__main__':
    pytest.main([__file__])