import pytest
import subprocess
from pathlib import Path
from click.testing import CliRunner
from unittest.mock import patch, MagicMock

from pydeptree.cli_advanced import (
    cli, 
    detect_file_type, 
    get_file_type_color, 
    get_file_type_icon,
    FileInfo
)


class TestConfigFileDetection:
    """Test config file type detection functionality"""
    
    def test_detect_config_by_filename(self):
        """Test config detection by specific filenames"""
        config_files = [
            'config.py',
            'settings.py', 
            'configuration.py',
            'env.py',
            'environment.py',
            'constants.py',
            'defaults.py',
            'local_settings.py',
            'dev_settings.py',
            'prod_settings.py',
            'test_settings.py'
        ]
        
        for filename in config_files:
            file_path = Path(f"/project/{filename}")
            assert detect_file_type(file_path) == 'config', f"Failed to detect {filename} as config"
    
    def test_detect_config_by_directory(self):
        """Test config detection by directory names"""
        config_dirs = [
            '/project/config/app.py',
            '/project/configs/database.py',
            '/project/settings/local.py'
        ]
        
        for dir_path in config_dirs:
            file_path = Path(dir_path)
            assert detect_file_type(file_path) == 'config', f"Failed to detect {dir_path} as config"
    
    def test_detect_config_by_keywords(self):
        """Test config detection by keywords in filename"""
        config_keywords = [
            'app_config.py',
            'db_settings.py',
            'api_configuration.py',
            'server_environment.py',
            'redis_env.py'
        ]
        
        for filename in config_keywords:
            file_path = Path(f"/project/{filename}")
            assert detect_file_type(file_path) == 'config', f"Failed to detect {filename} as config"
    
    def test_config_priority_over_other_types(self):
        """Test that config detection has priority over other types"""
        # Config in utils directory should be config, not utils
        file_path = Path("/project/utils/config.py")
        assert detect_file_type(file_path) == 'config'
        
        # Settings in models directory should be config, not model
        file_path = Path("/project/models/settings.py") 
        assert detect_file_type(file_path) == 'config'
    
    def test_non_config_files_unchanged(self):
        """Test that non-config files are still detected correctly"""
        test_cases = [
            (Path("/project/models/user.py"), 'model'),
            (Path("/project/services/api.py"), 'service'),
            (Path("/project/utils/helpers.py"), 'utils'),
            (Path("/project/tests/test_app.py"), 'test'),
            (Path("/project/main.py"), 'main'),
            (Path("/project/random.py"), 'other')
        ]
        
        for file_path, expected_type in test_cases:
            assert detect_file_type(file_path) == expected_type, f"{file_path} should be {expected_type}"


class TestConfigFileTypeFormatting:
    """Test config file type colors and icons"""
    
    def test_config_file_icon(self):
        """Test config file icon"""
        assert get_file_type_icon('config') == '⚙️'
    
    def test_config_file_color(self):  
        """Test config file color"""
        assert get_file_type_color('config') == 'bright_blue'
    
    def test_all_file_type_icons(self):
        """Test all file type icons are defined"""
        expected_icons = {
            'model': '📊',
            'service': '🌐', 
            'utils': '🔧',
            'test': '🧪',
            'main': '🚀',
            'config': '⚙️',
            'other': '📄'
        }
        
        for file_type, expected_icon in expected_icons.items():
            assert get_file_type_icon(file_type) == expected_icon
    
    def test_all_file_type_colors(self):
        """Test all file type colors are defined"""
        expected_colors = {
            'model': 'cyan',
            'service': 'green',
            'utils': 'yellow', 
            'test': 'magenta',
            'main': 'red',
            'config': 'bright_blue',
            'other': 'white'
        }
        
        for file_type, expected_color in expected_colors.items():
            assert get_file_type_color(file_type) == expected_color


class TestAdvancedCLIBasics:
    """Test basic functionality of advanced CLI"""
    
    def test_advanced_cli_help(self):
        """Test that advanced CLI help works"""
        runner = CliRunner()
        result = runner.invoke(cli, ['--help'])
        assert result.exit_code == 0
        assert 'Advanced Python Dependency Tree Analyzer' in result.output
    
    def test_advanced_cli_non_python_file(self):
        """Test advanced CLI with non-Python file"""
        runner = CliRunner() 
        with runner.isolated_filesystem():
            # Create a non-Python file
            Path('test.txt').write_text('not python')
            
            result = runner.invoke(cli, ['test.txt'])
            # Advanced CLI might handle non-Python files gracefully, so just check it doesn't crash
            assert result.exit_code == 0 or 'Error' in result.output
    
    @patch('pydeptree.cli_advanced.subprocess.run')
    def test_advanced_cli_basic_analysis(self, mock_run):
        """Test basic analysis functionality"""
        # Mock successful ruff execution
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout='[]',  # Empty JSON array = no lint issues
            stderr=''
        )
        
        runner = CliRunner()
        with runner.isolated_filesystem():
            # Create a simple Python file
            test_file = Path('test.py')
            test_file.write_text('''
def hello():
    return "world"
''')
            
            result = runner.invoke(cli, ['test.py', '--depth', '1'])
            # Should not crash (exit code 0 or reasonable error)
            assert result.exit_code == 0 or 'dependencies' in result.output


class TestIntegrationWithSampleConfig:
    """Test integration with sample config files"""
    
    def test_sample_config_files_detected(self):
        """Test that sample config files are detected correctly"""
        sample_project = Path(__file__).parent.parent / 'sample_project'
        
        if (sample_project / 'config.py').exists():
            config_file = sample_project / 'config.py'
            assert detect_file_type(config_file) == 'config'
        
        if (sample_project / 'utils' / 'config.py').exists():
            utils_config = sample_project / 'utils' / 'config.py'
            assert detect_file_type(utils_config) == 'config'
        
        if (sample_project / 'models' / 'settings.py').exists():
            settings_file = sample_project / 'models' / 'settings.py'
            assert detect_file_type(settings_file) == 'config'
    
    def test_sample_project_analysis_includes_config(self):
        """Test that analyzing sample project includes config files"""
        sample_project = Path(__file__).parent.parent / 'sample_project'
        main_file = sample_project / 'main.py'
        
        if main_file.exists():
            runner = CliRunner()
            result = runner.invoke(cli, [str(main_file), '--depth', '2', '--no-check-git'])
            
            # Should not crash and should include config files if they exist
            assert result.exit_code == 0
            if (sample_project / 'config.py').exists() or (sample_project / 'utils' / 'config.py').exists():
                assert '⚙️' in result.output  # Config icon should appear