from django import forms
from django.utils.translation import gettext_lazy as _

from .models import BidWindow, Bid


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['number_of_tokens', 'bidding_price', 'user', 'bid_window']
        widgets = {
            'user': forms.HiddenInput(),
            'bid_window': forms.HiddenInput(),
        }
