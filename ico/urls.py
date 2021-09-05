from django.urls import path, include

from .views import IndexView, BidWindowsView


app_name = 'ico'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('bid_windows/', BidWindowsView.as_view(), name='bid_windows'),
]
