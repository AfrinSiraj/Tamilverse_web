from django.db import models

class Place(models.Model):
    CATEGORY_CHOICES = [
        ('temple','Temple'),('church','Church'),('fort','Fort'),('palace','Palace'),('museum','Museum'),('nature','Nature'),('hill','Hill/Lake')
    ]
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    district = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='places/', blank=True, null=True)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    is_crowded = models.BooleanField(default=False)
    visit_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
