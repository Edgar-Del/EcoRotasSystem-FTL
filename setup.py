#!/usr/bin/env python3
"""
Setup do EcoRota Angola
======================

Configuração para instalação do pacote EcoRota Angola.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Ler README
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

# Ler requirements
requirements_path = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_path.exists():
    with open(requirements_path, 'r', encoding='utf-8') as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="ecorota-angola",
    version="1.0.0",
    author="Sistema EcoRota Angola",
    author_email="suporte@ecorota-angola.com",
    description="Sistema Inteligente de Recomendação de Rotas de Ecoturismo Sustentável",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ecorota-angola/ecorota-system",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.10",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
        "web": [
            "streamlit>=1.25.0",
            "streamlit-folium>=0.13.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "ecorota=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.csv", "*.json", "*.yaml", "*.yml"],
    },
    keywords=[
        "ecoturismo",
        "angola",
        "machine-learning",
        "recomendacao",
        "sustentabilidade",
        "otimizacao",
        "geografia",
        "turismo",
    ],
    project_urls={
        "Bug Reports": "https://github.com/ecorota-angola/ecorota-system/issues",
        "Source": "https://github.com/ecorota-angola/ecorota-system",
        "Documentation": "https://ecorota-angola.readthedocs.io/",
    },
)
