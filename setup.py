# python3 setup.py sdist bdist_wheel

import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="movie_magnet",
    version="0.0.3",
    description="Python tool to get magnet links to any movie",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/zahash/movie_magnet",
    author="zahash",
    author_email="zahash.z@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["movie_magnet"],
    include_package_data=True,
    install_requires=[
        "bs4",
        "requests",
        "pandas",
        "tabulate",
        "termcolor",
        "pyfiglet",
        "lxml",
    ],
    entry_points={"console_scripts": ["movie_magnet=movie_magnet.__main__:main",]},
)
