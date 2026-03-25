from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import TemplateView
from interactions.models import Like, Visit, Review

class RegisterView(View):
    def get(self, request):
        return render(request, 'auth/register.html')
    def post(self, request):
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        first_name = request.POST.get('first_name', '')
        if not username or password1 != password2:
            messages.error(request, 'Invalid registration details.')
            return redirect('accounts:register')
        from .models import User
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('accounts:register')
        user = User.objects.create_user(username=username, email=email, password=password1, first_name=first_name)
        login(request, user)
        return redirect('home')

class LoginView(View):
    def get(self, request):
        return render(request, 'auth/login.html')
    def post(self, request):
        user = authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'))
        if not user:
            messages.error(request, 'Invalid credentials.')
            return redirect('accounts:login')
        login(request, user)
        return redirect('home')

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('accounts:login')

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        likes = Like.objects.filter(user=user).select_related('place')
        visits = Visit.objects.filter(user=user).select_related('place').order_by('-timestamp')
        reviews = Review.objects.filter(user=user).select_related('place').order_by('-created_at')
        timeline = []
        for l in likes:
            timeline.append({'timestamp': l.created_at, 'action': 'liked', 'place_name': l.place.name})
        for v in visits:
            timeline.append({'timestamp': v.timestamp, 'action': 'visited', 'place_name': v.place.name})
        for r in reviews:
            timeline.append({'timestamp': r.created_at, 'action': 'reviewed', 'place_name': r.place.name})
        timeline.sort(key=lambda x: x['timestamp'], reverse=True)
        ctx.update(
            {
                'liked_places': likes,
                'visited_places': visits,
                'reviews': reviews,
                'timeline': timeline,
            }
        )
        return ctx

class SettingsView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'accounts/settings.html')

    def post(self, request):
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name).strip()
        user.email = request.POST.get('email', user.email).strip()
        user.bio = request.POST.get('bio', user.bio).strip()
        user.location = request.POST.get('location', user.location).strip()
        user.preferred_theme = request.POST.get('preferred_theme', user.preferred_theme)
        user.preferred_language = request.POST.get('preferred_language', user.preferred_language)
        if request.FILES.get('profile_image'):
            user.profile_image = request.FILES['profile_image']
        user.save()
        messages.success(request, 'Profile settings updated successfully.')
        return redirect('accounts:settings')
