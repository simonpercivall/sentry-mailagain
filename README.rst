sentry-mailagain
================

sentry-mailagain is a Sentry plugin to resend the mail notification on
receiving new events in an unresolved group. The mail notification will be
handled in the same manner as would a regression.

Installation
------------

> pip install sentry-mailagain

Configuration
-------------

Configuration is per-project, and has one setting: You may configure how long
the plugin should wait before treating new events for a group as needing a new
notification.

License
-------

sentry-mailagain is licensed under the BSD license.

Resources
---------

Bug tracker:
  https://github.com/simonpercivall/sentry-mailagain/issues

Source:
  https://github.com/simonpercivall/sentry-mailagain/
