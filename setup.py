from setuptools import setup, find_packages
from os import path

req_file = path.abspath('./requirements.txt')

setup(
    name='araceae',
    version='0.1.3',
    packages=find_packages(),
    install_requires=open(req_file, 'r').readlines(),
    extras_require={'dev': ['pytest', 'build']},
    entry_points={
        'console_scripts': [],
    },
    ext_modules=[]
)
