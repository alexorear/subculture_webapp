from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Publisher(models.Model):
    publisher_name = models.CharField(max_length = 30)

    def __str__(self):
        return self.publisher_name

class ComicTitle(models.Model):
    comic_title = models.CharField(max_length = 75)
    publisher = models.ForeignKey(Publisher, on_delete = models.CASCADE)
    reservations = models.IntegerField(default = 0)

    def __str__(self):
        return self.comic_title

class PullHold(models.Model):
    user = models.ForeignKey(User, related_name="reading")
    comic = models.ForeignKey(ComicTitle, related_name="likes")
