"""
Setup script for ARXML Editor.

Installs the ARXML Editor package and its dependencies.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README file
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

# Read requirements
requirements_file = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_file.exists():
    requirements = requirements_file.read_text(encoding="utf-8").strip().split('\n')
    requirements = [req.strip() for req in requirements if req.strip() and not req.startswith('#')]

setup(
    name="arxml-editor",
    version="0.1.0",
    description="Professional ARXML Editor with AUTOSAR compliance and advanced validation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="ARXML Editor Team",
    author_email="team@arxml-editor.com",
    url="https://github.com/arxml-editor/arxml-editor",
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-qt>=4.2.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "mypy>=1.0.0"
        ]
    },
    entry_points={
        "console_scripts": [
            "arxml-editor=arxml_editor.main:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Tools",
        "Topic :: Text Processing :: Markup :: XML",
    ],
    keywords="arxml autosar xml editor validation diagram",
    project_urls={
        "Bug Reports": "https://github.com/arxml-editor/arxml-editor/issues",
        "Source": "https://github.com/arxml-editor/arxml-editor",
        "Documentation": "https://arxml-editor.readthedocs.io/",
    },
)