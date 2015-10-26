from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.views.generic import DetailView, FormView, TemplateView
from tinyblog.forms import (
    EmailSubscriptionForm,
    UnsubscriptionConfirmationForm
)
from tinyblog.models import EmailSubscriber
from tinyblog.utils.mail import send_subscription_confirmation


class SubscriptionView(FormView):
    form_class = EmailSubscriptionForm
    template_name = 'tinyblog/subscribe.html'

    def form_valid(self, form):
        subscriber = form.save()
        self.request.session['tinyblog_thanks_uuid'] = str(
            subscriber.uuid_first
        )

        send_subscription_confirmation(subscriber)
        return HttpResponseRedirect(reverse('tinyblog_subscribe_thanks'))
subscribe = SubscriptionView.as_view()


class TinyBlogAcknowledgeSubscriptionView(DetailView):
    template_name = 'tinyblog/subscribe_thanks.html'
    context_object_name = 'subscriber'

    def get_object(self, queryset=None):
        return get_object_or_404(
            EmailSubscriber,
            uuid_first=self.request.session['tinyblog_thanks_uuid']
        )
acknowledge_subscription = TinyBlogAcknowledgeSubscriptionView.as_view()


def subscribe_confirm(request, uuid):
    subscriber = get_object_or_404(EmailSubscriber, uuid_second=uuid)
    subscriber.confirmed = True
    subscriber.save()

    return render_to_response('tinyblog/subscribe_confirmed.html',
                              {'subscriber': subscriber},
                              context_instance=RequestContext(request))


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
