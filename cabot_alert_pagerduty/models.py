# -*- coding: utf-8 -*-
import logging
import os
import pygerduty

from django.db import models
from cabot.cabotapp.alert import AlertPlugin, AlertPluginUserData


logger = logging.getLogger(__name__)


class PagerdutyAlert(AlertPlugin):
    '''
    This plugin is used for alerting to Pagerduty from Cabot.
    The implementation is a hack, because of the current
    pagerduty design. The alerting parameters are configured on
    a per-user basis and not per service. (hipchat, email, phone-no
    etc.)

    Once you install this plugin,
    1. add a user dedicated to pagerduty
    2. configure this user as "fallback duty officer"
    3. configure the service key in this user's profile
    '''
    name = "Pagerduty"
    author = "Mahendra M"

    @property
    def alert_status_list(self):
        if not hasattr(self, '_alert_status_list'):
            self._alert_status_list = _gather_alertable_status()

        return self._alert_status_list

    def send_alert(self, service, users, duty_officers):
        """Implement your send_alert functionality here."""

        if not self._service_alertable(service):
            return

        subdomain = os.environ.get('PAGERDUTY_SUBDOMAIN')
        api_token = os.environ.get('PAGERDUTY_API_TOKEN')

        client = pygerduty.PagerDuty(subdomain, api_token)

        description_prefix = 'Service: %s is %s' % (service.name,
                                             service.overall_status)

        users = service.users_to_notify.all()
        
        service_keys = []
        for userdata in PagerdutyAlertUserData.objects.filter(user__user__in=users):
            if userdata.service_key:
                service_keys.append(str(userdata.service_key))
                
        failed_checks = [check for check in service.all_failing_checks()]
        
        for failed_check in failed_checks:
            description = '%s failed check [%s]' % (description_prefix, failed_check.name)
            incident_key = '%s/%d/%d' % (service.name.lower().replace(' ', '-'),
                                  service.pk, failed_check.pk) 

            for service_key in service_keys:
                try:
                    if service.overall_status not in self.alert_status_list:
                        client.resolve_incident(service_key,
                                                incident_key)
                    else:
                        client.trigger_incident(service_key,
                                                alert_description,
                                                incident_key=incident_key)
                except Exception, exp:
                    logger.exception('Error invoking pagerduty: %s' % str(exp))
                    raise

    def _service_alertable(self, service):
        """ Evaluate service for alertable status """

        if service.overall_status in self.alert_status_list:
            return True

        if service.overall_status not in self.alert_status_list and \
            service.old_overall_status in self.alert_status_list:
            return True

        return False


def _gather_alertable_status():
    alert_status_list = os.environ.get('PAGERDUTY_ALERT_STATUS', 'CRITICAL').split(',')
    return alert_status_list


class PagerdutyAlertUserData(AlertPluginUserData):
    name = "Pagerduty Plugin"
    service_key = models.CharField(max_length=50, blank=True, null=True)
