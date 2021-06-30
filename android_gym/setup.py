#!/usr/bin/env python

# Third party
from setuptools import find_packages, setup

setup(
    name="gym_android",
    version="0.0.2",
    install_requires=["gym>=0.2.3", "pandas", "cfg_load"],
    packages=find_packages(),
)
