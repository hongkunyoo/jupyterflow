import os
from setuptools import setup, find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
# def read(fname):
#     return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="jupytermoon",
    version='0.0.1',
    author="hongkunyoo",
    author_email="hongkunyoo@gmail.com",
    description=read('README.md'),
    license="BSD 3-Clause",
    keywords="ctl, jupyterhub, pipeline, ML",
    packages=find_packages(),
    install_requires=['escapism', 'PyYAML', 'kubernetes', 'Jinja2', 'requests'],
    scripts=['jupytermoon']
)
