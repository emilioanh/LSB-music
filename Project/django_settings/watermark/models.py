from django.db import models

# Create your models here.
class Song(models.Model):
    name = models.CharField(null=True, blank=True, max_length=100)
    srcLink = models.CharField(null=True, blank=True, max_length=200)
    genre = models.CharField(null=True, blank=True, max_length=100)
    author = models.CharField(null=True, blank=True, max_length=100)
    # price = models.FloatField(default=0)

    class Meta:
        db_table = 'watermark_song'

    def __str__(self):
        if self.author is None:
            self.author = " "
        return self.author + " - " + self.name

    # def save(self, *args, **kargs):
    #     if self.link is None:
    #         self.link = "https://docs.google.com/uc?export=open&id="+self.id
    #     super(Song,self).save(*args, **kargs)

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    songs = models.ManyToManyField(Song)

    def __str__(self):
        return self.name + " - " + self.email