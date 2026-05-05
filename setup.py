from setuptools import setup, find_packages
import io

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="SchoolAPI",
    version="1.0.0",
    author="cubetitled-ui",
    author_email="cubetitled@gmail.com",
    description="Библиотека для удобной разработки проектов, связанных с МЭШ.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cubetitled-ui/SchoolAPI",
    packages=find_packages(),
    install_requires=[
        "aiohttp>=3.8.0",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)