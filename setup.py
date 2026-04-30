#!/usr/bin/env python3
"""
Setup script for DNS Benchmark Pro
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    if os.path.exists("README.md"):
        with open("README.md", "r", encoding="utf-8") as f:
            return f.read()
    return "DNS Benchmark Pro - Advanced DNS performance testing tool"

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="dns-benchmark-laboratory",
    version="1.0.0",
    author="DNS Benchmark Laboratory",
    author_email="contact@dnsbenchmarklaboratory.com",
    description="Advanced DNS performance testing tool with modern UI",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/dns-benchmark-pro",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Developers",
        "Topic :: Internet :: Name Service (DNS)",
        "Topic :: System :: Networking :: Monitoring",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "dns-benchmark=main:main",
            "dns-benchmark-laboratory=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.txt", "*.md"],
    },
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.20.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=0.991",
        ],
    },
    keywords="dns benchmark performance testing network latency",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/dns-benchmark-pro/issues",
        "Source": "https://github.com/yourusername/dns-benchmark-pro",
        "Documentation": "https://github.com/yourusername/dns-benchmark-pro/blob/main/README.md",
    },
)