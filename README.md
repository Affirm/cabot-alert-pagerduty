Cabot Pagerduty Plugin
=====
This is a pagerduty alert plugin for Cabot.

### Usage
This plugin is used for alerting to Pagerduty from Cabot. The implementation is a hack, because of the current pagerduty design. The alerting parameters are configured on a per-user basis and not per service. (hipchat, email, phone-no etc.)

Once you install this plugin,
* add a user dedicated to pagerduty
* configure this user as "fallback duty officer"
* configure the service key in this user's profile
