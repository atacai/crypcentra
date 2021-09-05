from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class BidWindow(models.Model):
    name = models.CharField(_("Bid Name"), max_length=50)
    total_tokens = models.IntegerField(_("Total Tokens"))
    start_time = models.DateTimeField(_("Start Time"), auto_now=False, auto_now_add=False)
    end_time = models.DateTimeField(_("End Time"), auto_now=False, auto_now_add=False)
    is_auctioned = models.BooleanField(_("Auction?"), default=False)

    def __str__(self):
        return self.name

    def validate_auction(self):
        if timezone.now() < self.end_time:
            raise ValidationError(_('Bid Window end time is not reached'))

    def auction(self):
        self.validate_auction()
        total_tokens = self.total_tokens
        for bid in self.window_bids.all().order_by('-bidding_price'):
            if not total_tokens:
                break
            if bid.success_tokens:
                pass
            same_price_bids = self.window_bids.filter(bidding_price=bid.bidding_price)
            if len(same_price_bids) > 1:
                for same_price_bid in same_price_bids.order_by('timestamp'):
                    if total_tokens > same_price_bid.number_of_tokens:
                        same_price_bid.success_tokens = same_price_bid.number_of_tokens
                        same_price_bid.save()
                        total_tokens -= bid.number_of_tokens
                    else:
                        same_price_bid.success_tokens = total_tokens
                        same_price_bid.save()
                        total_tokens = 0
            else:
                if total_tokens > bid.number_of_tokens:
                    bid.success_tokens = bid.number_of_tokens
                    bid.save()
                    total_tokens -= bid.number_of_tokens
                else:
                    bid.success_tokens = total_tokens
                    bid.save()
                    total_tokens = 0
        self.is_auctioned = True
        self.save()
        return self


class Bid(models.Model):
    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE, related_name='user_bids')
    number_of_tokens = models.IntegerField(_("Number of Tokens"))
    bidding_price = models.DecimalField(_("Bidding Price"), max_digits=32, decimal_places=2)
    timestamp = models.DateTimeField(_("Timestamp"), auto_now_add=True)
    success_tokens = models.IntegerField(_("Number of Success Tokens"), blank=True, null=True)
    bid_window = models.ForeignKey(BidWindow, on_delete=models.CASCADE, related_name='window_bids')

    def __str__(self):
        return '%s - %s' % (self.bid_window.name, self.user.username)

    def clean(self):
        if not self.bid_window.start_time < timezone.now() < self.bid_window.end_time:
            raise ValidationError(_('Bid Window is not ready to bid'))
        if self.number_of_tokens > self.bid_window.total_tokens:
            raise ValidationError(_('Invalid number of tokens'))
        return super().clean()
