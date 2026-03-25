from django.urls import path
from .views import ToggleLikeView, VisitPlaceView, AddReviewView

urlpatterns = [
    path('place/<slug:slug>/like/', ToggleLikeView.as_view(), name='toggle-like'),
    path('place/<slug:slug>/visit/', VisitPlaceView.as_view(), name='visit-place'),
    path('place/<slug:slug>/review/', AddReviewView.as_view(), name='add-review'),
]
