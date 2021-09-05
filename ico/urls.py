from django.urls import path, include

from .views import IndexView, BidWindowsView, BidWindowView, BidSummaryView


app_name = 'ico'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('bid_windows/', BidWindowsView.as_view(), name='bid_windows'),
    path('bid_windows/<int:pk>/', BidWindowView.as_view(), name='bids'),  
    path('bid_windows/<int:pk>/summary', BidSummaryView.as_view(), name='bids_summary'),  
]
