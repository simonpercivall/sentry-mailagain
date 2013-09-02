from datetime import timedelta
from threading import local

from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from sentry.plugins import plugins
from sentry.plugins.sentry_mail.models import MailPlugin
from sentry.plugins.bases.notify import NotificationPlugin
from sentry.tasks.post_process import plugin_post_process_group
from sentry.utils.safe import safe_execute

from . import __version__, __author__
from .forms import MailAgainConfForm
from .models import NotificationEvent


_notification_flag = local()


class MailAgainPlugin(NotificationPlugin):
    title = _('Mail Again')
    slug = 'mail_again'
    description = 'Re-mailing of unresolved events'
    version = __version__
    author = __author__
    author_url = 'https://github.com/simonpercivall/sentry-mailagain'
    
    conf_title = title
    conf_key = slug
    project_conf_form = MailAgainConfForm
    project_conf_template = "sentry_mailagain/project_configuration_form.html"

    def _last_notification_is_too_old(self, group):
        # TODO: check if enough time has gone by since the last
        #       notification to send a new notification
        too_old_age = self.get_option('mail_again_age', group.project)
        try:
            last_notification = NotificationEvent.objects.filter(group=group).latest()
        except NotificationEvent.DoesNotExist:
            return False

        if last_notification.notified_at < timezone.now() - timedelta(hours=too_old_age):
            return True
        
    def _register_notification(self, group):
        NotificationEvent.objects.create(group=group)

    def _resend_mail(self, group, event, is_sample, **kwargs):
        mail_plugin = plugins.get(MailPlugin.slug)
        if not safe_execute(mail_plugin.is_enabled, group.project):
            return
        
        plugin_post_process_group.delay(
            mail_plugin.slug,
            group=group,
            event=event,
            is_new=True,
            is_sample=is_sample,
            **kwargs
        )
        
        self._register_notification(group)

    def notify_users(self, group, event, fail_silently=False):
        self._register_notification(group)
        _notification_flag.was_notified = True

    def _should_mail_again(self, group, is_new):
        if not _notification_flag.was_notified and not is_new \
                and self._last_notification_is_too_old(group):
            return True
    
    def post_process(self, group, event, is_new, is_sample, **kwargs):
        # reset notification flag
        _notification_flag.was_notified = False

        super(MailAgainPlugin, self).post_process(group, event, is_new, is_sample, **kwargs)

        # if no notification were to be sent, and it's not a new event,
        # evaluate if we should force a notification anyway.
        if self._should_mail_again(group, is_new):
            self._resend_mail(group, event, is_sample, **kwargs)
