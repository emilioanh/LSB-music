from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Song(models.Model):
    id = models.CharField(max_length=20, primary_key=True, unique=True)
    name = models.CharField(null=True, blank=True, max_length=150)
    author = models.CharField(null=True, blank=True, max_length=100)
    srcLink = models.CharField(null=True, blank=True, max_length=250)
    genre = models.CharField(null=True, blank=True, max_length=100)
    fileType = models.CharField(blank=True, max_length=10)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    price = models.FloatField(default=0)

    class Meta:
        db_table = 'watermark_song'

    def __str__(self):
        return self.author + " - " + self.name

    def save(self, *args, **kargs):
        if self.srcLink is None:
            self.srcLink = "https://docs.google.com/uc?export=open&id="+self.id
        if self.author is "" or self.author is None:
            self.author = "Đang cập nhật"
        super(Song,self).save(*args, **kargs)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    songs = models.ManyToManyField(Song)
    folder_id = models.CharField(null=True, blank=True, max_length=40)

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def update_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()