# portal/models.py

from django.db import models

class Club(models.Model):
    name = models.CharField(max_length=100)        # Tên CLB
    description = models.TextField(blank=True)     # Mô tả
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
