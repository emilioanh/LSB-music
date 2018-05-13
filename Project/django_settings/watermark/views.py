from django.shortcuts import render
from APIs.drive_api_impl import save_files_to_sqlite
from watermark.models import Song

# Create your views here.
def home(request):
    # save_files_to_sqlite()
    songs = Song.objects.all()
    return render(request, 'index.html', {'songs':songs})