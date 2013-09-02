from django.forms import forms
from sentry.web.forms.fields import RangeField


class MailAgainConfForm(forms.Form):
    mail_again_age = RangeField(
        help_text=(
            "Send a new mail notification if an unresolved event is seen again "
            "and the last notification was older than this amount of time"
        ),
        required=False, min_value=0, max_value=168, step_value=1
    )
