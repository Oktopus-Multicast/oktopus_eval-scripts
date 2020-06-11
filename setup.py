"""Packaging settings."""
from setuptools import setup
from okevaluation import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name = 'oktopus_evaluation',
    version = __version__,
    author="Example Author",
    author_email="author@example.com",
    description = 'Oktopus evaluation.',
    long_description = long_description,
    long_description_content_type="text/markdown",
    url = 'https://cs-git-research.cs.surrey.sfu.ca/nsl/ISP/oktopus/eval-scripts',
    packages=['okevaluation'],
    classifiers = [
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
    ],
    entry_points = {
        'console_scripts': [
            'okevaluation=okevaluation.cli:main',
        ],
    }
)