"""Packaging settings."""
import os

from setuptools import setup
from okevaluation import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name = 'oktopus_evaluation',
    version = __version__,
    author='Khaled Diab, Carlos Lee',
    author_email='kdiab@sfu.ca, carlosl@sfu.ca',
    description = 'Oktopus evaluation.',
    long_description = long_description,
    long_description_content_type='text/markdown',
    url = 'https://github.com/Oktopus-Multicast/oktopus_eval-scripts.git',
    packages=['okevaluation'],
    install_requires=required,
    classifiers = [
        'License :: OSI Approved :: MIT License'
    ],
    entry_points = {
        'console_scripts': [
            'okevaluation=okevaluation.cli:main',
        ],
    }
)