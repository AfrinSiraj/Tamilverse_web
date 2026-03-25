from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from places.models import Place
from .models import Like, Visit, Review

class ToggleLikeView(LoginRequiredMixin, View):
    def _toggle(self, request, slug):
        place = get_object_or_404(Place, slug=slug)
        like, created = Like.objects.get_or_create(user=request.user, place=place)
        if not created:
            like.delete()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'liked': created})
        return redirect('place-detail', slug=slug)

    def post(self, request, slug):
        return self._toggle(request, slug)

    def get(self, request, slug):
        return self._toggle(request, slug)

class VisitPlaceView(LoginRequiredMixin, View):
    def post(self, request, slug):
        place = get_object_or_404(Place, slug=slug)
        Visit.objects.create(user=request.user, place=place)
        place.visit_count += 1
        place.save(update_fields=['visit_count'])
        return redirect('place-detail', slug=slug)

class AddReviewView(LoginRequiredMixin, View):
    def post(self, request, slug):
        place = get_object_or_404(Place, slug=slug)
        rating = int(request.POST.get('rating', 5))
        comment = request.POST.get('comment', '').strip()
        rating = max(1, min(5, rating))
        if comment:
            Review.objects.create(user=request.user, place=place, rating=rating, comment=comment)
        return redirect('place-detail', slug=slug)
