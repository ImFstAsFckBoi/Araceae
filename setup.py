from setuptools import setup, find_packages


setup(
    name='araceae',
    version='0.1.2',
    packages=find_packages(),
    install_requires=[
        'opencv-python',
        'numpy',
        'nptyping',
    ],
    extras_require={'dev': ['pytest', 'build']},
    entry_points={
        'console_scripts': [],
    },
    ext_modules=[]
)
