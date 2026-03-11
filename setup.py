"""
Setup script for sketchup-file-toolkit.
"""
from setuptools import setup, find_packages
from pathlib import Path

readme = Path("README.md").read_text(encoding="utf-8")

setup(
    name="sketchup-file-toolkit",
    version="1.0.0",
    description="Python library for working with SketchUp files",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Developer",
    author_email="dev@example.com",
    url="https://github.com/sketchup-tools/sketchup-file-toolkit",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "pathlib2>=2.3.0;python_version<'3.4'",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "sketchup_file_toolkit=sketchup_file_toolkit.main:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
