#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

setup(
    author="Adam Novotny",
    author_email='adam@adamnovotny.com',
    description="Description...",
    long_description=readme + '\n\n' + history,
    name='Name...',
    version='0.1.0',
    packages=['forecast_service'],
    entry_points={
        'console_scripts': [
            'forecast_service=forecast_service.wsgi:flask_default',
        ],
    },
    test_suite='tests',
    zip_safe=False,
)
