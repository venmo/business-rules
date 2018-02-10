#! /usr/bin/env python

import setuptools

from business_rules import __version__ as version

with open('HISTORY.rst') as f:
    history = f.read()

description = 'Python DSL for setting up business intelligence rules that can be configured without code; based on Venmo/business-rules.'

setuptools.setup(
        name='business-rules-extra',
        version=version,
        description='{0}'.format(description),
        author='Anna Winkler',
        author_email='me.anna.winkler@gmail.com',
        url='https://github.com/annawinkler/business-rules',
        packages=['business_rules'],
        license='MIT'
)
