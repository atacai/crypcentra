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
    