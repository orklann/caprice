"""
Caprice is a robust Python library for generating PDF.
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
    packages=find_packages(exclude=['tests', 'tests.*', 'resources']),
    include_package_data=True,
    package_data={'caprice': ['data/caprice/afm/*.afm', 
        'data/caprice/encoding/*.txt']},
    install_requires=["fonttools"],
    version=get_version(),
    url='https://github.com/orklann/caprice',
    description='Robust Python library for generating PDF',
    long_description=__doc__,
    author='Tommy Jeff',
    author_email='threcius@yahoo.com',
    license='GPLv2.0',
    platforms='any'
)
