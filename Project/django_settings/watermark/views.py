from django.shortcuts import render, redirect
from APIs.drive_api_impl import save_files_to_sqlite,uploadToFolder
from watermark.models import Song
from django.contrib.auth import login, authenticate
from watermark.forms import SignUpForm, UploadForm
from django.contrib.auth.decorators import login_required

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

@login_required()
def upload(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            author = form.cleaned_data['author']
            genre = form.cleaned_data['genre']
            price = form.cleaned_data['price']
            my_file = request.FILES['fileUpload']
            fileType = my_file.name.split('.')[1]
            #upload
            newFileId = uploadToFolder(my_file.name, my_file.temporary_file_path(), my_file.content_type)
            #save in db
            newSong = Song(id=newFileId, name=name, author=author, genre=genre, fileType=fileType, price=price)
            newSong.save()
            return redirect('homepage')
    else:
        form = UploadForm()
    return render(request, 'upload.html', {'form': form})