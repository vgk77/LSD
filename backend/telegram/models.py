from django.db import models


class Template(models.Model):
    name = models.CharField(max_length=256, unique=True)
    text = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
