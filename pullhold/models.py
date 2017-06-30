from django.db import models

# Create your models here.
class Publisher(models.Model):
    publisher_name = models.CharField(max_length = 30)

    def __str__(self):
        return self.publisher_name

class ComicTitle(models.Model):
    comic_title = models.CharField(max_length = 150)
    Publisher = models.ForeignKey(Publisher, on_delete = models.CASCADE)
    reservations = models.IntegerField(default = 0)

    def __str__(self):
        return self.comic_title
