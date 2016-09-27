#!/usr/bin/env python
from setuptools import setup

__VERSION__ = '1.0.2'

setup(name='cabot-alert-pagerduty',
      version=__VERSION__,
      description='Pagerduty alert plugin for Cabot',
      author='Mahendra',
      author_email='mahendra@affirm.com',
      url='http://cabotapp.com',
      packages=[
        'cabot_alert_pagerduty'
      ],
      download_url='https://github.com/Affirm/cabot-alert-pagerduty/tarball/%s' % __VERSION__,
      install_requires=[
        'pygerduty==0.14',
      ],
      tests_require=[
        'cabot',
      ],
     )
