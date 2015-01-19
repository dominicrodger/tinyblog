from django import forms
from tinyblog.models import EmailSubscriber


class EmailSubscriptionForm(forms.ModelForm):
    class Meta:
        model = EmailSubscriber
        exclude = ('confirmed', 'unsubscribed', )
