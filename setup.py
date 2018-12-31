#!/usr/bin/env python
from setuptools import setup, find_packages

__VERSION__ = '1.0.2'

setup(name='cabot-alert-pagerduty',
      version=__VERSION__,
      description='Pagerduty alert plugin for Cabot',
      author='Mahendra',
      author_email='mahendra@affirm.com',
      url='http://cabotapp.com',
      packages=find_packages(),
      download_url='https://github.com/Affirm/cabot-alert-pagerduty/tarball/%s' % __VERSION__,
      install_requires=[
        'pygerduty==0.14',
      ],
     )
