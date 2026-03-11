"""
Configuration for sketchup-file-toolkit.
"""
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"

# Software settings
SOFTWARE_NAME = "SketchUp"
SUPPORTED_EXTENSIONS = ['.blend', '.max', '.c4d', '.obj', '.fbx', '.stl']

# Processing settings
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB
BATCH_SIZE = 100
VERBOSE = False
