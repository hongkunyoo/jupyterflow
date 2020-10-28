import os, re
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
    'requests',
    'click',
    'jinja2-ansible-filters',
    'jsonpath-ng'
]

def get_version():
    init = open(os.path.join(ROOT, 'jupyterflow', '__init__.py')).read()
    return VERSION_RE.search(init).group(1)


setup(
    name="jupyterflow",
    version=get_version(),
    author="hongkunyoo",
    author_email="hongkunyoo@gmail.com",
    description="Run your workflow on JupyterHub",
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    url='https://github.com/hongkunyoo/jupyterflow',
    license="BSD 3-Clause",
    keywords="ctl, jupyterhub, pipeline, ML",
    packages=find_packages(),
    # package_data={'jupyterflow': ['templates/*']},
    install_requires=requires,
    include_package_data=True,
    scripts=['bin/jupyterflow']
)
