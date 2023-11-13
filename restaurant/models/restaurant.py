import uuid

from django.db import models

from restaurant.models.owner import Owner


class Restaurant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='restaurants')
    page_url = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
