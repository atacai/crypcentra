import datetime
from datetime import datetime as dt

from django.core.exceptions import ValidationError
from django.contrib.auth.models import User, make_password
from django.test import TestCase
from django.utils import timezone

from .models import BidWindow, Bid


class BidWindowValidationTestCase(TestCase):

    def setUp(self):
        self.bid_window = BidWindow.objects.create(name='TestICO', total_tokens=10, start_time=timezone.now() + datetime.timedelta(days=1), end_time=timezone.now() + datetime.timedelta(days=2))
        self.user = User.objects.create(username='test_user', password=make_password('test_password'))

    def test_bidwindow_can_bid(self):
        bid = Bid(user=self.user, number_of_tokens=10, bidding_price=1.00, bid_window=self.bid_window)
        with self.assertRaises(ValidationError):
            bid.full_clean()

    def test_bidwindow_validate_auction(self):
        with self.assertRaises(ValidationError):
            self.bid_window.validate_auction()

    def test_bidwindow_totaltokens(self):
        self.bid_window.start_time = timezone.now() - datetime.timedelta(days=1)
        self.bid_window.save()
        bid = Bid(user=self.user, number_of_tokens=20, bidding_price=1.00, bid_window=self.bid_window)
        with self.assertRaises(ValidationError):
            bid.full_clean()


class BidWindowAuctionTestCase(TestCase):

    def setUp(self):
        super().setUp()
        self.bid_window = BidWindow.objects.create(name='TestICO', total_tokens=10, start_time=timezone.now() - datetime.timedelta(days=1), end_time=timezone.now() + datetime.timedelta(days=1))
        self.user1 = User.objects.create(username='test_user1', password=make_password('test_password'))
        self.user2 = User.objects.create(username='test_user2', password=make_password('test_password'))
        self.user3 = User.objects.create(username='test_user3', password=make_password('test_password'))

    def test_bidwindow_auction_price(self):
        Bid.objects.create(user=self.user1, number_of_tokens=5, bidding_price=1.00, bid_window=self.bid_window)
        Bid.objects.create(user=self.user2, number_of_tokens=5, bidding_price=3.00, bid_window=self.bid_window)
        Bid.objects.create(user=self.user3, number_of_tokens=5, bidding_price=2.00, bid_window=self.bid_window)
        self.bid_window.end_time = timezone.now() - datetime.timedelta(hours=1)
        self.bid_window.save()
        self.bid_window.auction()
        bid1 = Bid.objects.get(user=self.user1)
        bid2 = Bid.objects.get(user=self.user2)
        bid3 = Bid.objects.get(user=self.user3)
        self.assertEqual(bid1.success_tokens, 0)
        self.assertEqual(bid2.success_tokens, 5)
        self.assertEqual(bid3.success_tokens, 5)

    def test_bidwindow_auction_price(self):
        Bid.objects.create(user=self.user1, number_of_tokens=5, bidding_price=1.00, bid_window=self.bid_window)
        Bid.objects.create(user=self.user2, number_of_tokens=5, bidding_price=3.00, bid_window=self.bid_window)
        Bid.objects.create(user=self.user3, number_of_tokens=5, bidding_price=1.00, bid_window=self.bid_window)
        self.bid_window.end_time = timezone.now() - datetime.timedelta(hours=1)
        self.bid_window.save()
        self.bid_window.auction()
        bid1 = Bid.objects.get(user=self.user1)
        bid2 = Bid.objects.get(user=self.user2)
        bid3 = Bid.objects.get(user=self.user3)
        self.assertEqual(bid1.success_tokens, 5)
        self.assertEqual(bid2.success_tokens, 5)
        self.assertEqual(bid3.success_tokens, 0)
