from django.core.urlresolvers import reverse, reverse_lazy
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, FormView, TemplateView
from tinyblog.forms import (
    EmailSubscriptionForm,
    UnsubscriptionConfirmationForm
)
from tinyblog.models import EmailSubscriber
from tinyblog.utils.mail import (
    send_subscription_confirmation,
    send_subscription_invitation
)


class SubscriptionView(FormView):
    form_class = EmailSubscriptionForm
    template_name = 'tinyblog/subscribe.html'
    submit_url = reverse_lazy('tinyblog_subscribe')

    def notify_subscription(self, subscriber):
        send_subscription_confirmation(subscriber)

    def get_context_data(self, **kwargs):
        ctx = super(SubscriptionView, self).get_context_data(**kwargs)
        ctx['submit_url'] = self.submit_url
        return ctx

    def form_valid(self, form):
        subscriber = form.save()
        self.request.session['tinyblog_thanks_uuid'] = str(
            subscriber.uuid_first
        )

        self.notify_subscription(subscriber)

        return HttpResponseRedirect(reverse('tinyblog_subscribe_thanks'))
subscribe = SubscriptionView.as_view()


class InviteSubscriptionView(SubscriptionView):
    submit_url = reverse_lazy('tinyblog_invite')

    def notify_subscription(self, subscriber):
        send_subscription_invitation(subscriber)
invite = InviteSubscriptionView.as_view()


class AcknowledgeSubscriptionView(DetailView):
    template_name = 'tinyblog/subscribe_thanks.html'
    context_object_name = 'subscriber'

    def get_object(self, queryset=None):
        uuid = self.request.session.get('tinyblog_thanks_uuid', None)

        if uuid is None:
            raise Http404

        return get_object_or_404(
            EmailSubscriber,
            uuid_first=uuid
        )
acknowledge_subscription = AcknowledgeSubscriptionView.as_view()


class SubscriptionConfirmView(DetailView):
    model = EmailSubscriber
    template_name = 'tinyblog/subscribe_confirmed.html'
    context_object_name = 'subscriber'

    def get_object(self, queryset=None):
        # This is a bit icky - we're modifying the subscription
        # information inside an HTTP GET request.
        subscriber = get_object_or_404(
            EmailSubscriber,
            uuid_second=self.kwargs['uuid']
        )
        subscriber.confirmed = True
        subscriber.save()

        return subscriber
subscribe_confirm = SubscriptionConfirmView.as_view()


class UnsubscriptionView(FormView):
    template_name = 'tinyblog/unsubscribe_form.html'
    form_class = UnsubscriptionConfirmationForm
    success_url = reverse_lazy('tinyblog_unsubscribe_thanks')

    def form_valid(self, form):
        EmailSubscriber.objects.filter(
            email=form.cleaned_data['email'],
            confirmed=True,
            unsubscribed=False
        ).update(unsubscribed=True)

        return super(UnsubscriptionView, self).form_valid(form)
unsubscribe = UnsubscriptionView.as_view()


class UnsubscriptionThanksView(TemplateView):
    template_name = 'tinyblog/unsubscribe.html'
unsubscribe_thanks = UnsubscriptionThanksView.as_view()
