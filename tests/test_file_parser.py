"""
Tests for sketchup-file-toolkit.
"""
import pytest
import tempfile
from pathlib import Path

from src.file_parser import FileParserManager


@pytest.fixture
def manager():
    """Create manager instance for testing."""
    return FileParserManager(verbose=False)


@pytest.fixture
def temp_dir():
    """Create temporary directory for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


class TestFileParserManager:
    """Tests for FileParserManager class."""
    
    def test_initialization(self, manager):
        """Test manager initialization."""
        assert manager is not None
        assert manager.config is not None
        assert "version" in manager.config
    
    def test_config_defaults(self, manager):
        """Test default configuration."""
        assert manager.config.get("software") == "SketchUp"
        assert "extensions" in manager.config
    
    def test_scan_empty_directory(self, manager, temp_dir):
        """Test scanning empty directory."""
        results = manager.scan(str(temp_dir))
        assert results == []
    
    def test_scan_nonexistent_directory(self, manager):
        """Test scanning non-existent directory."""
        with pytest.raises(FileNotFoundError):
            manager.scan("/nonexistent/path")
    
    def test_process_empty(self, manager, temp_dir):
        """Test processing empty directory."""
        output_dir = temp_dir / "output"
        results = manager.process(str(temp_dir), str(output_dir))
        
        assert results["processed"] == 0
        assert results["errors"] == 0
        assert (output_dir / "report.json").exists()


class TestUtils:
    """Tests for utility functions."""
    
    def test_format_size(self):
        """Test size formatting."""
        from src.utils import format_size
        
        assert "B" in format_size(100)
        assert "KB" in format_size(1024)
        assert "MB" in format_size(1024 * 1024)
    
    def test_sanitize_filename(self):
        """Test filename sanitization."""
        from src.utils import sanitize_filename
        
        assert sanitize_filename("test<>file.txt") == "test__file.txt"
        assert sanitize_filename("normal.txt") == "normal.txt"
    
    def test_ensure_dir(self, temp_dir):
        """Test directory creation."""
        from src.utils import ensure_dir
        
        new_dir = temp_dir / "new" / "nested" / "dir"
        result = ensure_dir(str(new_dir))
        
        assert result.exists()
        assert result.is_dir()
