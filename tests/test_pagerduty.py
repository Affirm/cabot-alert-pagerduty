# -*- coding: utf-8 -*-
import os
from cabot.cabotapp.alert import AlertPlugin
from cabot.plugin_test_utils import PluginTestCase
from mock import patch, call

from cabot.cabotapp.models import Service, UserProfile
from cabot_alert_pagerduty import models


class TestPagerdutyAlerts(PluginTestCase):
    def setUp(self):
        super(TestPagerdutyAlerts, self).setUp()

        self.alert = AlertPlugin.objects.get(title=models.PagerdutyAlert.name)
        self.service.alerts.add(self.alert)
        self.service.save()

        self.plugin = models.PagerdutyAlert.objects.get()

        # self.user's service key is user_key
        models.PagerdutyAlertUserData.objects.create(user=self.user.profile, service_key='user_key')

    def test_critical_alertable(self):
        """ A service with a critical status is alertable """
        self.service.overall_status = self.service.CRITICAL_STATUS
        self.assertTrue(self.plugin._service_alertable(self.service))

    def test_non_critical_alertable(self):
        """ A non-critical service status does not alert """
        for status in Service.WARNING_STATUS, Service.ERROR_STATUS:
            self.service.overall_status = status
            self.assertFalse(self.plugin._service_alertable(self.service))

    def test_default_critical_status(self):
        os.environ.pop('PAGERDUTY_ALERT_STATUS', None)
        default_alert_status = ['CRITICAL']
        self.assertEqual(default_alert_status, models._gather_alertable_status())

    def test_default_status_in_plugin(self):
        os.environ.pop('PAGERDUTY_ALERT_STATUS', None)
        default_alert_status = ['CRITICAL']
        self.assertEqual(default_alert_status, self.plugin.alert_status_list)

    def test_configured_status_in_plugin(self):
        os.environ['PAGERDUTY_ALERT_STATUS'] = 'CRITICAL,WARNING'
        custom_alert_status = ['CRITICAL', 'WARNING']
        self.assertEqual(custom_alert_status, self.plugin.alert_status_list)

    @patch('cabot_alert_pagerduty.models.pygerduty.PagerDuty')
    def test_trigger_and_resolve(self, fake_client_class):
        resolve_incident = fake_client_class.return_value.resolve_incident
        trigger_incident = fake_client_class.return_value.trigger_incident

        self.transition_service(Service.PASSING_STATUS, Service.CRITICAL_STATUS)
        trigger_incident.assert_called_once_with('user_key', 'Service: Service is CRITICAL',
                                                 incident_key='service/2194')

        self.transition_service(Service.CRITICAL_STATUS, Service.PASSING_STATUS)
        resolve_incident.assert_called_once_with('user_key', 'service/2194')

    @patch('cabot_alert_pagerduty.models.pygerduty.PagerDuty')
    def test_alert_multiple_schedules(self, fake_client_class):
        trigger_incident = fake_client_class.return_value.trigger_incident

        # self.fallback_officer's key is fallback_key, alert self.user and self.fallbak_officer
        models.PagerdutyAlertUserData.objects.create(user=self.fallback_officer.profile, service_key='fallback_key')
        self.service.users_to_notify.add(self.fallback_officer)

        self.transition_service(Service.PASSING_STATUS, Service.CRITICAL_STATUS)
        trigger_incident.assert_has_calls([
            call('user_key', 'Service: Service is CRITICAL', incident_key='service/2194'),
            call('fallback_key', 'Service: Service is CRITICAL', incident_key='service/2194'),
        ])
