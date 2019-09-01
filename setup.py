#!/usr/bin/env python
from distutils.core import setup

INSTALL_REQUIRES = ["beautifulsoup4", "requests"]

PYTHON_REQUIRES = ">=3.4"

setup(
    name="calorizator_parser",
    version="0.1",
    description="Calorizator site parser application",
    packages=["calorizator_parser"],
    install_requires=INSTALL_REQUIRES,
    python_requires=PYTHON_REQUIRES,
)
