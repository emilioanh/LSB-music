import time, os
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from mimetypes import MimeTypes
from APIs.drive_api_impl import save_files_to_sqlite, uploadToFolder, downloadFile, createFolder
from watermark import lsb
from watermark.models import Song, Profile
from watermark.forms import SignUpForm, UploadForm, DecodeForm

# Create your views here.
def home(request):
    songs = Song.objects.filter(ownuser__exact=None)
    if not songs:
        save_files_to_sqlite()
        songs = Song.objects.filter(ownuser__exact=None)
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

@login_required()
def buy(request, song_id):
    #get required data
    user = User.objects.get(pk=request.session['userid'])
    rawSong = Song.objects.get(pk=song_id)
    #download song
    fileName = f"{rawSong.name} - {rawSong.author}.{rawSong.fileType}"
    downloadedPath = downloadFile(fileId=song_id, fileName=fileName)
    #LSB this fucking song
    watermarkMess = f"Bought by {user.username} on {time.ctime()}"
    encode = lsb.GiautinLSB()
    encodedFilePath = encode.run(filepath=downloadedPath, stega_text=watermarkMess, newfileName=fileName)
    #Upload to user folder
    mime = MimeTypes()
    content_type, thrVar = mime.guess_type(encodedFilePath)
    if user.profile.folder_id:
        folder_id = user.profile.folder_id
    else:
        folder_id = createFolder(user.username)
        user.profile.folder_id = folder_id
        user.profile.save()
    newFileId = uploadToFolder(name=fileName, path=encodedFilePath, mimetype=content_type, folderId=folder_id)
    #delete songs on local machine
    os.remove(downloadedPath)
    os.remove(encodedFilePath)
    #write the new song in the user songs list in db
    newSong = Song(id=newFileId, name=rawSong.name, author=rawSong.author, genre=rawSong.genre, fileType=rawSong.fileType, price=rawSong.price, ownuser=user)
    newSong.save()
    user.profile.songs.add(newSong)
    user.profile.save()
    
    return redirect('mysong')

@login_required()
def mysong(request):
    user = User.objects.get(pk=request.session['userid'])
    songs = Song.objects.filter(ownuser__exact=user)
    return render(request, 'auths/mysong.html', {'songs':songs})

def decode(request):
    if request.POST:
        form = DecodeForm(request.POST, request.FILES)
        if form.is_valid():
            musicFile = form.cleaned_data['fileUpload']
            decoder = lsb.GiaimaLSB(musicFile.temporary_file_path())
            watermarkMess = decoder.get_text()
            print("File: ", musicFile, " Temp path: ", musicFile.temporary_file_path(), " Mess: ", watermarkMess)
            messages.info(request, f"Your watermark for this song is: {watermarkMess}")
    else:
        form = DecodeForm()
    return render(request, 'decode.html', {'form': form})