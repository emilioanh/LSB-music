from django.db import models

# Create your models here.
class Song(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(null=True, blank=True, max_length=100)
    srcLink = models.CharField(null=True, blank=True, max_length=200)
    genre = models.CharField(null=True, blank=True, max_length=100)
    author = models.CharField(null=True, blank=True, max_length=100)
    # price = models.FloatField(default=0)

    class Meta:
        db_table = 'watermark_song'

    def __str__(self):
        if self.author is None:
            self.author = "Đang cập nhật"
        return self.author + " - " + self.name

    def save(self, *args, **kargs):
        if self.srcLink is None:
            self.srcLink = "https://docs.google.com/uc?export=open&id="+self.id
        super(Song,self).save(*args, **kargs)

class User(models.Model):
    email = models.EmailField(blank=True, null=True)
    name = models.CharField(max_length=100)
    songs = models.ManyToManyField(Song)

    def __str__(self):
        return self.name + " - " + self.email