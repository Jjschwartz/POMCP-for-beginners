import sys
from setuptools import setup

assert sys.version_info.major == 3 and sys.version_info.minor >= 7, \
    "The pypomcp package is designed to work with Python 3.7 and greater." \
    + "Please install it before proceeding."

setup(name='pypomcp',
      version='0.0.1',
      install_requires=[],
      description="A python implementation of the POMCP algorithm for the learning.",
      author="Jonathon Schwartz")
