#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unittest

import tests.bootstrap_tests

from cabot.cabotapp.models import Service
from cabot_alert_pagerduty.models import PagerdutyAlert
# from cabot_alert_pagerduty.models import _service_alertable
from cabot_alert_pagerduty.models import _gather_alertable_status

class TestServiceStatusChecks(unittest.TestCase):

    def setUp(self):
        pass

    def test_critical_alertable(self):
        """ A service with a critical status is alertable """
        service = Service()

        plugin = PagerdutyAlert()

        service.overall_status = service.CRITICAL_STATUS
        self.assertTrue(plugin._service_alertable(service))

    def test_non_critical_alertable(self):
        """ A non-critical service status does not alert """
        service = Service()

        plugin = PagerdutyAlert()

        service.overall_status = service.WARNING_STATUS
        self.assertFalse(plugin._service_alertable(service))

        service.overall_status = service.ERROR_STATUS
        self.assertFalse(plugin._service_alertable(service))

    def test_default_critical_status(self):

        os.environ.pop('PAGERDUTY_ALERT_STATUS', None)

        default_alert_status = ['CRITICAL']
        self.assertEqual(default_alert_status, _gather_alertable_status())

    def test_default_status_in_plugin(self):

        os.environ.pop('PAGERDUTY_ALERT_STATUS', None)

        default_alert_status = ['CRITICAL']
        plugin = PagerdutyAlert()

        self.assertEqual(default_alert_status, plugin.alert_status_list)

    def test_configured_status_in_plugin(self):

        os.environ['PAGERDUTY_ALERT_STATUS'] = 'CRITICAL,WARNING'

        custom_alert_status = ['CRITICAL', 'WARNING']
        plugin = PagerdutyAlert()

        self.assertEqual(custom_alert_status, plugin.alert_status_list)

if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestServiceStatusChecks)
    unittest.TextTestRunner(verbosity=2).run(SUITE)
