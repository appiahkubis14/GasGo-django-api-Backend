from django.urls import path
from .views import ConsumerListCreateView, ConsumerDetailView

urlpatterns = [
    path('consumers/', ConsumerListCreateView.as_view(), name='consumer-list-create'),
    path('consumers/<int:pk>/', ConsumerDetailView.as_view(), name='consumer-detail'),
]
