from setuptools import setup, find_packages
import glob
import os

with open('requirements.txt') as f:
    required = [x for x in f.read().splitlines() if not x.startswith("#")]

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'Readme.md'), encoding='utf-8') as f:
    long_description = f.read()

# Note: the _program variable is set in __init__.py.
# it determines the name of the command line tool.
from series_sleuth import __version__, _program

setup(
    name='blaseball-series-sleuth',
    version=__version__,
    packages=['series_sleuth'],
    package_data = {
      'series_sleuth': ['data/*.json']
    },
    description='blaseball-series-sleuth is a command line utility for getting info about blaseball series',
    url='https://github.com/ch4zm/blaseball-series-sleuth',
    author='Ch4zm of Hellmouth',
    author_email='ch4zm.of.hellmouth@gmail.com',
    license='MIT',
    entry_points="""
    [console_scripts]
    {program} = series_sleuth.command:main
    """.format(program = _program),
    install_requires=required,
    keywords=[],
    zip_safe=False,
    long_description=long_description,
    long_description_content_type='text/markdown'
)
