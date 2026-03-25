import json
import re
from pathlib import Path

from django.core.management.base import BaseCommand
from django.conf import settings

from places.models import Place


def _default_name_from_file(filename):
    stem = filename[:-5].strip()
    stem = stem.replace(".", " ")
    stem = re.sub(r"([a-z])([A-Z])", r"\1 \2", stem)
    return re.sub(r"\s+", " ", stem).strip()


def _category_from_name(name):
    lowered = name.lower()
    if "temple" in lowered:
        return "temple"
    if "church" in lowered or "basilica" in lowered:
        return "church"
    if "fort" in lowered:
        return "fort"
    if "palace" in lowered:
        return "palace"
    if "museum" in lowered:
        return "museum"
    if "beach" in lowered or "kulam" in lowered or "town hall" in lowered:
        return "nature"
    return "hill"


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        base_dir = Path(settings.BASE_DIR)
        slug_map_path = base_dir / "places" / "slug_map.json"
        data = json.loads(slug_map_path.read_text(encoding="utf-8"))
        file_map = data.get("files", {})

        # Parse lat/lon + district hints from original explore cards.
        explore_path = base_dir / "frontend" / "auth" / "explore.html"
        explore_html = explore_path.read_text(encoding="utf-8", errors="ignore")
        card_data = {}
        card_pattern = re.compile(
            r"<a href=\"\.\./pages/(?P<file>[^\"]+)\">[\s\S]*?<div class=\"card [^\"]+\" data-lat=\"(?P<lat>[^\"]+)\" data-lon=\"(?P<lon>[^\"]+)\">[\s\S]*?<h4>(?P<name>.*?)</h4>[\s\S]*?<p>(?P<district>.*?)</p>",
            re.IGNORECASE,
        )
        for match in card_pattern.finditer(explore_html):
            card_data[match.group("file")] = {
                "name": match.group("name").strip(),
                "district": match.group("district").strip() or "Tamil Nadu",
                "lat": float(match.group("lat")),
                "lon": float(match.group("lon")),
            }

        created = 0
        updated = 0
        for filename, slug in file_map.items():
            fallback_name = _default_name_from_file(filename)
            info = card_data.get(filename, {})
            name = info.get("name") or fallback_name
            district = info.get("district") or "Tamil Nadu"
            lat = info.get("lat", 0.0)
            lon = info.get("lon", 0.0)
            category = _category_from_name(name)

            obj, was_created = Place.objects.update_or_create(
                slug=slug,
                defaults={
                    "name": name,
                    "district": district,
                    "description": f"{name} heritage site in {district}.",
                    "category": category,
                    "latitude": lat,
                    "longitude": lon,
                },
            )
            if was_created:
                created += 1
            else:
                updated += 1

        self.stdout.write(self.style.SUCCESS(f"Seed complete: {created} created, {updated} updated"))
