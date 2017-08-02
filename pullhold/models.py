from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Publisher(models.Model):
    publisher_name = models.CharField(max_length = 30)

    def __str__(self):
        return self.publisher_name

class ComicTitle(models.Model):
    comic_title = models.CharField(max_length = 75)
    publisher = models.ForeignKey(Publisher, on_delete = models.CASCADE)
    reservations = models.IntegerField(default = 0)
    cover_art = models.CharField(max_length = 250, blank = True)
    readers = models.ManyToManyField('UserProfile', through='ComicReaders', blank = True)


    def __str__(self):
        return self.comic_title + ' - ' + self.publisher.publisher_name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    bio = models.TextField(max_length = 500, blank = True)
    comics = models.ManyToManyField(ComicTitle, related_name="pullhold_list", through='ComicReaders', blank = True)

    def __str__(self):
        return self.user.username

    #methods to automatically create a UserProfile when a user login is created
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.userprofile.save()

#this links comictitles and readers together so they can easily be viewed in admin panel
class ComicReaders(models.Model):
    ComicTitle = models.ForeignKey(ComicTitle)
    UserProfile = models.ForeignKey(UserProfile)

    class Meta:
        db_table = 'pullhold_comictitle_readers'
        auto_created = User.get_full_name
