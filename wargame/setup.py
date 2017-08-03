#!/usr/bin/env python3


from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf8') as f:
    long_description = f.read()

setup(
    name='wargame',
    version='0.1.0',
    description='Game engine for computer wargames',
    long_description='Game engine based on Pygame and Python to make implementation of turn based games much simpler.',
    url='https://github.com/maximinus/wargame',
    author='Chris Handy',
    author_email='maximinus@gmail.com',
    license='GPL3',
    classifiers=['Development Status :: 3 - Alpha',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python :: 3.5',
                 'Topic :: Games/Entertainment :: Turn Based Strategy',
                 'Topic :: Software Development :: Libraries :: pygame'],
    keywords='pygame framework boardgame strategy',
    packages=find_packages(exclude=[]),
    install_requires=['pyyaml>=3.12',
                      'pygame>=1.9.3',
                      'python-box>=3.0.1'],
    python_requires='>=3')
