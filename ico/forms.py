from django import forms
from django.utils.translation import gettext_lazy as _

from .models import BidWindow, Bid


class BidWindowAuctionForm(forms.Form):
    bid_window_id = forms.IntegerField()

    def save(self):
        try:
            window = BidWindow.objects.get(id=self.cleaned_data.get('bid_window_id'))
        except:
            raise forms.ValidationError(_('No Bid Window found'))
        window.auction()


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['number_of_tokens', 'bidding_price', 'user', 'bid_window']
        widgets = {
            'user': forms.HiddenInput(),
            'bid_window': forms.HiddenInput(),
        }
