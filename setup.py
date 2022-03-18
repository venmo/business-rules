#! /usr/bin/env python
from setuptools import setup

from business_rules import __version__ as version

with open('README.md') as f:
    readme = f.read()

with open('HISTORY.md') as f:
    history = f.read()

setup(
    name='business-rules',
    version=version,
    description='Python DSL for setting up business intelligence rules that can be configured without code',
    long_description='{}\n\n{}'.format(readme, history),
    long_description_content_type='text/markdown',
    author='Venmo',
    author_email='open-source@venmo.com',
    url='https://github.com/venmo/business-rules',
    packages=['business_rules'],
    license='MIT',
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*",
    install_requires=[
        "six>=1.16.0",
    ],
)
