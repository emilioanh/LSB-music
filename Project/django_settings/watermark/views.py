from django.shortcuts import render, redirect
from APIs.drive_api_impl import save_files_to_sqlite
from watermark.models import Song
from django.contrib.auth import login, authenticate
from watermark.forms import SignUpForm

# Create your views here.
def home(request):
    # save_files_to_sqlite()
    songs = Song.objects.all()
    return render(request, 'index.html', {'songs':songs})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('homepage')
    else:
        form = SignUpForm()
    return render(request, 'auths/signup.html', {'form': form})