#!/usr/bin/env python3
"""
Cambridge Isotope Laboratories 多线程爬虫安装脚本
"""

from setuptools import setup, find_packages
import os

# 读取 README 文件
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# 读取依赖
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="cambridge-isotope-scraper",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="高效的多线程爬虫工具，用于提取 Cambridge Isotope Laboratories 产品信息",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/youngbee12/cambridge-isotope-scraper",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "isotope-scraper=optimized_multithreaded_scraper:main",
            "isotope-test=high_thread_test:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["examples/*", "*.md", "*.txt"],
    },
    keywords="scraping, chemistry, isotopes, selenium, multithreading",
    project_urls={
        "Bug Reports": "https://github.com/youngbee12/cambridge-isotope-scraper/issues",
        "Source": "https://github.com/youngbee12/cambridge-isotope-scraper",
        "Documentation": "https://github.com/youngbee12/cambridge-isotope-scraper#readme",
    },
)
