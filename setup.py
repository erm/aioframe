import os
from setuptools import find_packages, setup

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='aioframe',
    version='0.0.1',
    packages=['aioframe'],
    install_requires=[
        'aiohttp',
        'aiohttp-jinja2',
        'aiohttp_session',
        'aioredis',
        'cryptography',
        'peewee==2.10.2',
        'peewee-async',
        'aiopg',
        'psycopg2-binary',
        'passlib',
    ],
    license='MIT License',
    author='Jordan E.',
    author_email='jermff@gmail.com',
)