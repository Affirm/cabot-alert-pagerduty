#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

import unittest

import tests.bootstrap_tests

from cabot.cabotapp.models import Service
from cabot_alert_pagerduty.models import _service_alertable

class TestServiceStatusChecks(unittest.TestCase):

    def setUp(self):
        pass

    def test_critical_alertable(self):
        """ A service with a critical status is alertable """
        service = Service()

        service.overall_status = service.CRITICAL_STATUS
        self.assertTrue(_service_alertable(service))

    def test_non_critical_alertable(self):
        """ A non-critical service status does not alert """
        service = Service()

        service.overall_status = service.WARNING_STATUS
        self.assertFalse(_service_alertable(service))

        service.overall_status = service.ERROR_STATUS
        self.assertFalse(_service_alertable(service))


if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestServiceStatusChecks)
    unittest.TextTestRunner(verbosity=2).run(SUITE)
