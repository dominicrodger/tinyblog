from django.core.exceptions import ValidationError
from django import forms
from tinyblog.models import EmailSubscriber


class EmailSubscriptionForm(forms.ModelForm):
    class Meta:
        model = EmailSubscriber
        exclude = ('confirmed', 'unsubscribed', )


def validate_subscribed_address(value):
    try:
        EmailSubscriber.objects.get(email=value)
    except EmailSubscriber.DoesNotExist:
        raise ValidationError(
            u'%s is not currently subscribed.' % value
        )


class UnsubscriptionConfirmationForm(forms.Form):
    email = forms.EmailField(
        help_text='The email address you wish to unsubscribe.',
        validators=[validate_subscribed_address, ]
    )
