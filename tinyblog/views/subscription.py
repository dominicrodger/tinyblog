from django.core.mail import EmailMultiAlternatives
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.template.loader import render_to_string
from django.views.generic import DetailView
from tinyblog.forms import EmailSubscriptionForm, EmailSubscriber
from tinyblog.utils import get_from_email, get_site_name


def subscribe(request):
    if request.method == 'GET':
        form = EmailSubscriptionForm()
        return render_to_response('tinyblog/subscribe.html',
                                  {'form': form},
                                  context_instance=RequestContext(request))
    else:
        form = EmailSubscriptionForm(request.POST)

        if form.is_valid():
            model = form.save()
            request.session['tinyblog_thanks_uuid'] = str(model.uuid_first)

            site = get_site_name()

            subject = 'Thanks for subscribing to {0}'.format(site)

            text_template = 'tinyblog/emails/confirm_subscription.txt'
            text_content = render_to_string(text_template,
                                            {'user': model, 'site': site})

            html_template = 'tinyblog/emails/confirm_subscription.html'
            html_content = render_to_string(html_template,
                                            {'user': model, 'site': site})

            to = model.email
            msg = EmailMultiAlternatives(subject, text_content,
                                         get_from_email(), [to, ])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            return HttpResponseRedirect(reverse('tinyblog_subscribe_thanks'))

        return render_to_response('tinyblog/subscribe.html',
                                  {'form': form},
                                  context_instance=RequestContext(request))


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


def unsubscribe(request, uuid):
    subscriber = get_object_or_404(EmailSubscriber, uuid_second=uuid)
    subscriber.unsubscribed = True
    subscriber.save()

    return render_to_response('tinyblog/unsubscribe.html',
                              {'subscriber': subscriber},
                              context_instance=RequestContext(request))
