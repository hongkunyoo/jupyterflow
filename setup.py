import os
from setuptools import setup, find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


ROOT = os.path.dirname(__file__)
VERSION_RE = re.compile(r'''__version__ = ['"]([0-9.]+)['"]''')


requires = [
    'escapism',
    'PyYAML',
    'kubernetes',
    'Jinja2',
    'requests'
]

def get_version():
    init = open(os.path.join(ROOT, 'jupytermoon', '__init__.py')).read()
    return VERSION_RE.search(init).group(1)


setup(
    name="jupytermoon",
    version=get_version(),
    author="hongkunyoo",
    author_email="hongkunyoo@gmail.com",
    description="Run your ML pipeline with jupytermoon",
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    url='https://github.com/hongkunyoo/jupytermoon',
    license="BSD 3-Clause",
    keywords="ctl, jupyterhub, pipeline, ML",
    packages=find_packages(),
    install_requires=requires,
    include_package_data=True,
    scripts=['bin/jupytermoon']
)
