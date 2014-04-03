#! /usr/bin/env python

import setuptools

from business_rules import __version__ as version

setuptools.setup(
        name='business-rules',
        version=version,
        description='Python DSL for setting up business intelligence rules that can be configured without code',
        author='Venmo',
        author_email='open-source@venmo.com',
        packages=['business_rules'],
)
