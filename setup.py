from distutils.core import setup
from setuptools import find_packages
import os

# Optional project description in README.md:
current_directory = os.path.dirname(os.path.abspath(__file__))

try:
    with open(os.path.join(current_directory, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
except Exception:
    long_description = ''

setup(

scripts = [    
],
# Project name: 
name='arikaim-client',

# Packages to include in the distribution: 
packages = [
    'arikaim.client'
],
   
# Project version number:
version='1.0.11',

# List a license for the project, eg. MIT License
license='MIT License',

# Short description of your library: 
description='Arikaim CMS api client',

# Long description of your library: 
long_description=long_description,
long_description_content_type='text/markdown',

# Your name: 
author='Intersoft Ltd',

# Your email address:
author_email='info@arikaim.com',

# Link to your github repository or website: 
url='https://github.com/arikaim/api-client-py',

# Download Link from where the project can be downloaded from:
download_url='',
# List of keywords: 
keywords=['arikaim', 'arikaim cms', 'api client'],

# List project dependencies: 
install_requires=[   
    'requests'
],

# https://pypi.org/classifiers/ 
classifiers=[
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
]
)