from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from places.views import HomeView, ExploreView, AboutView, ContactView, PlaceDetailView, ChatbotAPIView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', HomeView.as_view(), name='home'),
    path('explore/', ExploreView.as_view(), name='explore'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('place/<slug:slug>/', PlaceDetailView.as_view(), name='place-detail'),

    path('accounts/', include('accounts.urls')),
    path('interactions/', include('interactions.urls')),


    # 🔥 chatbot (correct path)
    path('api/chatbot/', ChatbotAPIView.as_view(), name='api-chatbot'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)