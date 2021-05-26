"""
Caprice is a robust PDF generation library for Python
"""

from setuptools import find_packages, setup

setup(
    name='caprice',
    packages=find_packages(include=['caprice']),
    version='0.1.0',
    url='https://github.com/orklann/caprice'
    description='Robust PDF generation library for Python',
    long_description=__doc__,
    author='Aaron Elkins',
    author_email='threcius@yahoo.com',
    license='GPLv2.0',
    platforms='any'
)