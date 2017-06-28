from django.db import models


class Tag(models.Model):
    word = models.CharField(max_length=60)
    slug = models.CharField(max_length=60)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.word
