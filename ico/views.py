from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import *

from .forms import BidWindowAuctionForm, BidForm
from .models import BidWindow, Bid


class IndexView(RedirectView):
    pattern_name = 'ico:bid_windows'


class BidWindowsView(FormView, ListView):
    model = BidWindow
    form_class = BidWindowAuctionForm
    success_url = '/bid_windows/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class BidWindowView(LoginRequiredMixin, FormView, DetailView):
    model = BidWindow
    form_class = BidForm
    success_url = '/bid_windows/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class BidSummaryView(LoginRequiredMixin, DetailView):
    model = BidWindow
    template_name = 'ico/bidwindow_summary.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_bids'] = self.object.window_bids.all()
        context['success_bids'] = self.object.window_bids.filter(success_tokens__isnull=False, success_tokens__gt=0)
        context['fail_bids'] = self.object.window_bids.filter(success_tokens__isnull=True, success_tokens=0)
        return context
    