Cabot Pagerduty Plugin
=====
This is a pagerduty alert plugin for Cabot.

### Usage
This plugin is used for alerting to Pagerduty from Cabot. The implementation is
a hack, because of the current pagerduty design. The alerting parameters are
configured on a per-user basis and not per service. (hipchat, email, phone-no etc.)

###Once you install this plugin:
####In PagerDuty:
* Create a V1 API Token. This will be needed for the Cabot configuration
value ```PAGERDUTY_API_TOKEN```
* Create a new Service. Add a Generic API integration. An Integration or
Service Key will be generated to be used for creating the specific user
to link to the PagerDuty escalation policy. Which users are alerted by
Pagerduty will be configured as part of this policy.

####In Cabot Configuration:
* Set ```PAGERDUTY_API_TOKEN``` to value configured in Pagerduty
* Set ```PAGERDUTY_SUBDOMAIN``` for Pagerduty API endpoint
* If alerts should be sent to Pagerduty for a service status check other than
critical, configure a comma-separated list for ```PAGERDUTY_ALERT_STATUS```
e.g. 'ERROR,CRITICAL'

####In Cabot:
* Add a user dedicated to a specific Pagerduty Escalation Policy
* Configure this user as "fallback duty officer"
* Configure the service key in this user's profile
