#! /usr/bin/env python

import setuptools

from business_rules import __version__ as version

with open('README.mdt') as f:
    readme = f.read()

with open('HISTORY.rst') as f:
    history = f.read()

setuptools.setup(
        name='business-rules',
        version=version,
        description='Python DSL for setting up business intelligence rules that can be configured without code',
        long_description='{0}\n\n{1}'.format(readme, history),
        long_description_content_type='text/markdown',
        author='Venmo',
        author_email='open-source@venmo.com',
        url='https://github.com/venmo/business-rules',
        packages=['business_rules'],
        license='MIT'
)
