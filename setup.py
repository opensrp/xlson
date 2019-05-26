# -*- coding: utf-8 -*-
"""
xlson - Convert an XLSForm to native form JSON.
"""
from setuptools import find_packages, setup

REQUIRES = ["click", "pyxform"]

setup(
    name="xlson",
    version="0.0.1",
    author="github.com/opensrp",
    author_email="info@smartregister.org",
    packages=find_packages(),
    url="https://github.com/opensrp/xlson",
    description="A Python package to convert XLSForms to native form JSON.",
    long_description=open("README.rst", "rt").read(),
    install_requires=REQUIRES,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    entry_points={"console_scripts": ["xlson=xlson:cli"]},
)
