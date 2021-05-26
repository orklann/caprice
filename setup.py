"""
Caprice is a robust PDF generation library for Python
"""
import os
from setuptools import find_packages, setup

def get_version():
    basedir = os.path.dirname(__file__)
    try:
        with open(os.path.join(basedir, 'caprice/version.py')) as f:
            locals = {}
            exec(f.read(), locals)
            return locals['VERSION']
    except FileNotFoundError:
        raise RuntimeError('No version info found.')

setup(
    name='caprice',
    packages=find_packages(include=['caprice']),
    version=get_version(),
    url='https://github.com/orklann/caprice',
    description='Robust PDF generation library for Python',
    long_description=__doc__,
    author='Aaron Elkins',
    author_email='threcius@yahoo.com',
    license='GPLv2.0',
    platforms='any'
)