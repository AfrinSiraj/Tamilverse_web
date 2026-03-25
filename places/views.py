import json
from pathlib import Path

from django.http import Http404
from django.shortcuts import render
from django.views.generic import DetailView, TemplateView

from interactions.models import Like, Review
import re

from django.http import JsonResponse
from django.views import View
from .models import Place

BASE_DIR = Path(__file__).resolve().parent.parent
SLUG_MAP_PATH = BASE_DIR / "places" / "slug_map.json"


def _load_slug_maps():
    if not SLUG_MAP_PATH.exists():
        return {}, {}
    data = json.loads(SLUG_MAP_PATH.read_text(encoding="utf-8"))
    return data.get("files", {}), data.get("aliases", {})

class HomeView(TemplateView):
    template_name = 'auth/index.html'

class AboutView(TemplateView):
    template_name = 'auth/about.html'

class ContactView(TemplateView):
    template_name = 'auth/contact.html'

class ExploreView(TemplateView):
    template_name = 'auth/explore.html'
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        qs = Place.objects.all()
        category = self.request.GET.get('category')
        crowded = self.request.GET.get('crowded')
        district = self.request.GET.get('district')
        most_visited = self.request.GET.get('most_visited')
        if category:
            qs = qs.filter(category=category)
        if crowded in ('true','false'):
            qs = qs.filter(is_crowded=(crowded == 'true'))
        if district:
            qs = qs.filter(district__icontains=district)
        if most_visited:
            qs = qs.order_by('-visit_count')
        ctx['places'] = qs
        return ctx

class PlaceDetailView(DetailView):
    model = Place
    context_object_name = 'place'

    def _template_for_place(self, place):
        file_map, alias_map = _load_slug_maps()
        reverse_file_map = {slug: fname for fname, slug in file_map.items()}
        reverse_alias_map = {slug: fname for fname, slug in alias_map.items()}
        filename = reverse_file_map.get(place.slug) or reverse_alias_map.get(place.slug)
        if not filename:
            compact_slug = place.slug.replace("-", "")
            for slug, fname in reverse_file_map.items():
                if slug.replace("-", "") == compact_slug:
                    filename = fname
                    break
        if not filename:
            raise Http404("Place page template not found.")
        return f"pages/{filename}"

    def render_to_response(self, context, **response_kwargs):
        template_name = self._template_for_place(context["place"])
        return render(self.request, template_name, context, **response_kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        place = self.object
        weather = None
        if place.latitude and place.longitude:
            try:
                import requests
                url = f"https://api.open-meteo.com/v1/forecast?latitude={place.latitude}&longitude={place.longitude}&current=temperature_2m,weather_code"
                data = requests.get(url, timeout=8).json()
                c = data.get('current', {})
                weather = {'temperature': c.get('temperature_2m'), 'description': f"Code {c.get('weather_code')}"}
            except Exception:
                weather = None
        ctx['weather'] = weather
        ctx['reviews'] = Review.objects.filter(place=place).select_related('user').order_by('-created_at')
        ctx['liked'] = self.request.user.is_authenticated and Like.objects.filter(user=self.request.user, place=place).exists()
        return ctx

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        if request.user.is_authenticated:
            place = self.object
            from interactions.models import Visit

            Visit.objects.create(user=request.user, place=place)
            place.visit_count += 1
            place.save(update_fields=["visit_count"])
        return response

def _request_data(request):
    if request.content_type and "application/json" in request.content_type:
        try:
            return json.loads(request.body.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            return {}
    return request.POST


class ChatbotAPIView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            message = (data.get("message") or "").lower()

            from .models import Place

            # 🔍 Detect district/place
            district = None
            places = Place.objects.all()

            for p in places:
                if p.district and p.district.lower() in message:
                    district = p.district
                    break

            # Default picks
            if district:
                picks = Place.objects.filter(district__icontains=district)[:6]
            else:
                picks = Place.objects.all()[:6]

            # -------------------------------
            # 🎯 INTENT LOGIC
            # -------------------------------

            # 🗺️ TRAVEL PLAN
            if "plan" in message or "itinerary" in message or "days" in message:
                days = 3
                import re
                match = re.search(r"(\d+)", message)
                if match:
                    days = int(match.group(1))

                itinerary = []
                idx = 0

                for d in range(1, days + 1):
                    day_places = picks[idx:idx+3]
                    idx += 3

                    stops = []
                    for p in day_places:
                        stops.append(p.name)

                    if not stops:
                        stops = ["Free exploration"]

                    itinerary.append(f"Day {d}: " + ", ".join(stops))

                return JsonResponse({
                    "reply": "\n".join(itinerary)
                })

            # 📍 NEARBY PLACES
            elif "near" in message or "nearby" in message:
                names = [p.name for p in picks]
                return JsonResponse({
                    "reply": "Nearby places:\n- " + "\n- ".join(names)
                })

            # 🍽️ FOOD
            elif "food" in message or "eat" in message:
                return JsonResponse({
                    "reply": "Try local foods like dosa, idli, meals, and street food near major attractions."
                })

            # 🏨 HOTELS
            elif "hotel" in message or "stay" in message:
                return JsonResponse({
                    "reply": "Budget hotels are available near city centers and tourist places."
                })

            # 🚗 TRANSPORT
            elif "transport" in message or "how to go" in message:
                return JsonResponse({
                    "reply": "Use bus, auto, or train. Local autos are best for short distances."
                })

            # 🌤️ BEST TIME / FESTIVAL
            elif "best time" in message or "festival" in message:
                return JsonResponse({
                    "reply": "Best time is Nov–Feb. Festivals like Pongal and temple festivals are popular."
                })

            # 🧠 GENERAL PLACE INFO
            else:
                if picks:
                    p = picks[0]
                    return JsonResponse({
                        "reply": f"{p.name} is a famous place in {p.district}. It is known for tourism and culture."
                    })

                return JsonResponse({
                    "reply": "Tell me what you want (places, food, travel plan, etc.)"
                })

        except Exception as e:
            print("CHATBOT ERROR:", e)
            return JsonResponse({"reply": "Server error"}, status=500)