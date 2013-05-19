from django.forms import ModelForm
from tinyblog.models import EmailSubscriber


class EmailSubscriptionForm(ModelForm):
    class Meta:
        model = EmailSubscriber
        exclude = ('confirmed', 'unsubscribed', )
