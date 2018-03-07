import os
from setuptools import find_packages, setup

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='aioframe',
    version='0.0.1',
    packages=['aioframe'],
    install_requires=[
        'aiohttp',
    ],
    license='MIT License',
    author='Jordan E.',
    author_email='jermff@gmail.com',
)