#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name='exif2pandas',
    version='1.5',

    description="Extract EXIF to pandas / SQL / Excel / Feather",
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="Visgean",
    author_email='visgean@gmail.com',
    url='https://github.com/visgean/exif2pandas',
    packages=[
        'exif2pandas',
    ],
    package_dir={'exif2pandas': 'exif2pandas'},
    license="MIT",
    keywords='exif sql',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
    install_requires=[
        'exifread==2.3.2',
        'pandas',
        'python-slugify',
    ],
    entry_points={
        'console_scripts': [
            'exif2pandas = exif2pandas.main:main'
        ]
    },
)