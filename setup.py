from setuptools import setup, Extension
from os import path

req_file = path.abspath('./requirements.txt')

setup(
    install_requires=open(req_file, 'r').readlines(),
)
