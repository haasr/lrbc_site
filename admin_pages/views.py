from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage

from lrbc_site import settings
from api import views as api_views
from site_pages.models import Page, Visitor
from site_pages import views as site_views
from site_pages import form_sender
from .models import *
from .forms import *

import os
import re

STATIC_DIR = settings.STATICFILES_DIRS[0]

ABOUT_HEADER_DIR       = STATIC_DIR + '/site_pages/about/header_image/'
ABOUT_BOX1_IMG_DIR     = STATIC_DIR + '/site_pages/about/box1_image/'
ABOUT_BOX2_IMG_DIR     = STATIC_DIR + '/site_pages/about/box2_image/'
ABOUT_GALLERY_IMGS_DIR = STATIC_DIR + '/site_pages/about/gallery_images/'
BACKGROUND_DIR         = STATIC_DIR + '/site_pages/home/bg_image/'
CONTACT_HEADER_DIR     = STATIC_DIR + '/site_pages/contact/header_image/'
HOME_GALLERY_IMGS_DIR  = STATIC_DIR + '/site_pages/home/gallery_images/'
MUSIC_AUDIO_DIR        = STATIC_DIR + '/site_pages/resources/worship_music/audio/'
MUSIC_HEADER_DIR       = STATIC_DIR + '/site_pages/resources/worship_music/header_image/'
NAV_ICON_DIR           = STATIC_DIR + '/site_pages/site_look/nav_image/'
ROBOTS_TXT_DIR         = settings.BASE_DIR + '/templates/'
SERMONS_AUDIO_DIR      = STATIC_DIR + '/site_pages/resources/sermons/audio/'
SERMONS_HEADER_DIR     = STATIC_DIR + '/site_pages/resources/sermons/header_image/'
SERVICES_HEADER_DIR    = STATIC_DIR + '/site_pages/services/header_image/'
SERVICES_BOX1_IMG_DIR  = STATIC_DIR + '/site_pages/services/box1_image/'
SERVICES_BOX2_IMG_DIR  = STATIC_DIR + '/site_pages/services/box2_image/'
SERVICES_BOX3_IMG_DIR  = STATIC_DIR + '/site_pages/services/box3_image/'
STATIC_IMGS_DIR        = STATIC_DIR + '/images/'
VIDEOS_HEADER_DIR      = STATIC_DIR + '/site_pages/resources/worship_videos/header_image/'
VIDEOS_BULLETINS_DIR    = STATIC_DIR + '/site_pages/resources/worship_videos/bulletins/'


@login_required
def admin_index(request):
    """Provides the landing page template for admins (not actual Django admins
    but those who can access the pages in this menu and the API URLS). The landing
    page serves as a menu to all the different templates to manage the site.

    Parameters:
    request (HttpRequest): An HTTP Request object. 

    Returns:
    HttpResponse: Directs the user to the appropriate URL.
    """
    current_user = request.user.first_name

    context = {'current_user': current_user}
    return render(request, 'admin_pages/index.html', context)


def try_delete_files(path):
    """Attempts to delete all files in the directory, path.

    Parameters:
    path (string): the file path from which to remove all files.

    Returns:
    bool: Indicates whether all file deletions succeeded or not.
    """
    failure = False
    try:
        for root, dirs, files in os.walk(path):
            for f in files:
                try:
                    os.remove(os.path.join(root, f))
                except:
                    failure = True
        return failure
    except:
        return False


@login_required
def manage_site_look(request):
    """Provides the user a form template to edit the data of the SiteLook
    object (for nav, footer, and page access) with id 1.

    Parameters:
    request (HttpRequest): An HTTP Request object. 

    Returns:
    HttpResponse: Directs the user to the appropriate URL depending on the request method.
    """
    site_look = SiteLook.objects.get(id=1)

    if (request.method != 'POST'):
        form = SiteLookForm(instance=site_look)
    else:
        fs_storage = FileSystemStorage(location=NAV_ICON_DIR)
        form = SiteLookForm(instance=site_look, data=request.POST)

        if len(request.FILES) != 0:
            if('navigation_img' in request.FILES.keys()):
                try_delete_files(NAV_ICON_DIR)

                image = request.FILES['navigation_img']
                fs_storage.save('nav_image.png', image)

            if('favicon' in request.FILES.keys()):
                fs_storage = FileSystemStorage(location=STATIC_IMGS_DIR)
                try:
                    os.remove(os.path.join(STATIC_IMGS_DIR, 'favicon.ico'))
                except:
                    pass

                image = request.FILES['favicon']
                fs_storage.save('favicon.ico', image)

        if (form.is_valid()):
            form.save()
            api_views.update_pages_allowed()

        return HttpResponseRedirect(reverse('admin_pages:admin_index'))

    context = { 'site_look': site_look, 'form': form }
    return render(request, 'admin_pages/manage_site_look/manage_site_look.html', context)


@login_required
def manage_home(request):
    """Provides the user a form template to edit the data of the Home
    object (for landing page content) with id 1.

    Parameters:
    request (HttpRequest): An HTTP Request object. 

    Returns:
    HttpResponse: Directs the user to the appropriate URL depending on the request method.
    """
    home = Home.objects.get(id=1)

    if (request.method != 'POST'):
		# no data submitted; createVIDEOS blank form.
        form = HomeForm(instance=home)
    else:
        form = HomeForm(instance=home, data=request.POST)

        if (form.is_valid()):
            form.save()

            data = form.cleaned_data
            # Delete existing gallery images if flag is true:
            if (data['delete_gallery']):
                try_delete_files(HOME_GALLERY_IMGS_DIR)

            if (len(request.FILES) != 0):
                if ('background_img' in request.FILES):
                    fs_storage = FileSystemStorage(location=BACKGROUND_DIR)
                    try_delete_files(BACKGROUND_DIR)

                    image = request.FILES['background_img']
                    filename = fs_storage.save('background.png', image)

                if('gallery_imgs' in request.FILES):
                    fs_storage = FileSystemStorage(location=HOME_GALLERY_IMGS_DIR)
                    gallery_files = request.FILES.getlist('gallery_imgs')

                    for f in gallery_files:
                        fs_storage.save(f.name, f)

            return HttpResponseRedirect(reverse('admin_pages:admin_index'))

    context = { 'home': home, 'form': form }
    return render(request, 'admin_pages/manage_home/manage_home.html', context)


@login_required
def manage_about(request):
    """Provides the user a form template to edit the data of the About
    object (for About page content) with id 1.

    Parameters:
    request (HttpRequest): An HTTP Request object. 

    Returns:
    HttpResponse: Directs the user to the appropriate URL depending on the request method.
    """
    about = About.objects.get(id=1)

    if (request.method != 'POST'):
        form = AboutForm(instance=about)
    else:
        form = AboutForm(instance=about, data=request.POST)

        if (form.is_valid()):
            form.save()

            data = form.cleaned_data
            # Delete existing gallery images if flag is true:
            if (data['delete_gallery']):
                try_delete_files(ABOUT_GALLERY_IMGS_DIR)

            if (about.delete_box1_img):
                about.box1_img_file_name = ''
                try_delete_files(ABOUT_BOX1_IMG_DIR)

            if (about.delete_box2_img):
                about.box2_img_file_name = ''
                try_delete_files(ABOUT_BOX2_IMG_DIR)

            if (len(request.FILES) != 0):
                if('header_image' in request.FILES):
                    try_delete_files(ABOUT_HEADER_DIR)
                    fs_storage = FileSystemStorage(location=ABOUT_HEADER_DIR)
                    image = request.FILES['header_image']
                    filename = fs_storage.save(image.name, image)
                    about.header_image_file_name = filename
                    about.save()

                if('gallery_imgs' in request.FILES):
                    fs_storage = FileSystemStorage(location=ABOUT_GALLERY_IMGS_DIR)
                    gallery_files = request.FILES.getlist('gallery_imgs')

                    for f in gallery_files:
                        fs_storage.save(f.name, f)

                if ('box1_img' in request.FILES):
                    try_delete_files(ABOUT_BOX1_IMG_DIR)
                    fs_storage = FileSystemStorage(location=ABOUT_BOX1_IMG_DIR)
                    image = request.FILES['box1_img']
                    about.box1_img_file_name = image.name
                    fs_storage.save(image.name, image)

                if ('box2_img' in request.FILES):
                    try_delete_files(ABOUT_BOX2_IMG_DIR)
                    fs_storage = FileSystemStorage(location=ABOUT_BOX2_IMG_DIR)
                    image = request.FILES['box2_img']
                    about.box2_img_file_name = image.name
                    fs_storage.save(image.name, image)

            about.save()

            return HttpResponseRedirect(reverse('admin_pages:admin_index'))

    context = { 'about': about, 'form': form }
    return render(request, 'admin_pages/manage_about/manage_about.html', context)


@login_required
def manage_resources(request):
    """Provides the user a template to control the content that would appear
    on the Sermons, Worship Music, and Worship Videos pages. Allows CRUD operations
    for Speaker, Artist, Sermon, Song, and WorshipVideo objects.

    Parameters:
    request (HttpRequest): An HTTP Request object. 

    Returns:
    HttpResponse: Directs the user to the appropriate URL to display the template.
    """
    speakers = Speaker.objects.all().order_by('name')
    artists = Artist.objects.all().order_by('name')
    sermons = Sermon.objects.all().order_by('date')
    songs = Song.objects.all().order_by('date')
    worship_videos = WorshipVideo.objects.all().order_by('date')

    context = { 
        'speakers': speakers, 'artists': artists, 
        'sermons': sermons, 'songs': songs,
        'worship_videos': worship_videos
        }
    return render(request, 'admin_pages/manage_resources/manage_resources.html', context)


@login_required
def manage_sermons_header(request):
    """Provides the user a form template to edit the header of the SermonsHeader
    object (for the Sermons page header) with id 1.

    Parameters:
    request (HttpRequest): An HTTP Request object. 

    Returns:
    HttpResponse: Directs the user to the appropriate URL depending on the vaidity of the form.
    """
    sermons_header = SermonsHeader.objects.get(id=1)

    if (request.method != 'POST'):
        form = SermonsHeaderForm(instance=sermons_header)
    else:
        fs_storage = FileSystemStorage(location=SERMONS_HEADER_DIR)
        form = SermonsHeaderForm(instance=sermons_header, data=request.POST)

        if (form.is_valid()):
            form.save()

            if len(request.FILES) != 0:
                try_delete_files(SERMONS_HEADER_DIR)
                image = request.FILES['header_image']
                filename = fs_storage.save(image.name, image)
                sermons_header.header_image_file_name = filename
                sermons_header.save()
            
            return HttpResponseRedirect(reverse('admin_pages:manage_resources'))

    context = { 'form': form }
    return render(request, 'admin_pages/manage_resources/sermons/manage_sermons_header.html', context)


@login_required
def manage_worship_music_header(request):
    """Provides the user a form template to edit the header of the MusicHeader
    object (for the Worship Music page header) with id 1.

    Parameters:
    request (HttpRequest): An HTTP Request object. 

    Returns:
    HttpResponse: Directs the user to the appropriate URL depending on the vaidity of the form.
    """
    music_header = MusicHeader.objects.get(id=1)

    if (request.method != 'POST'):
        form = MusicHeaderForm(instance=music_header)
    else:
        fs_storage = FileSystemStorage(location=MUSIC_HEADER_DIR)
        form = MusicHeaderForm(instance=music_header, data=request.POST)

        if (form.is_valid()):
            form.save()

            if len(request.FILES) != 0:
                try_delete_files(MUSIC_HEADER_DIR)
                image = request.FILES['header_image']
                filename = fs_storage.save(image.name, image)
                music_header.header_image_file_name = filename
                music_header.save()
            
            return HttpResponseRedirect(reverse('admin_pages:manage_resources'))

    context = { 'form': form }
    return render(request, 'admin_pages/manage_resources/worship_music/manage_worship_music_header.html', context)


@login_required
def manage_worship_videos_header(request):
    """Provides the user a form template to edit the header of the VideosHeader
    object (for the Worship Videos page header) with id 1.

    Parameters:
    request (HttpRequest): An HTTP Request object. 

    Returns:
    HttpResponse: Directs the user to the appropriate URL depending on the vaidity of the form.
    """
    videos_header = VideosHeader.objects.get(id=1)

    if (request.method != 'POST'):
        form = VideosHeaderForm(instance=videos_header)
    else:
        fs_storage = FileSystemStorage(location=VIDEOS_HEADER_DIR)
        form = VideosHeaderForm(instance=videos_header, data=request.POST)
        
        if (form.is_valid()):
            form.save()

            if len(request.FILES) != 0:
                try_delete_files(VIDEOS_HEADER_DIR)
                image = request.FILES['header_image']
                filename = fs_storage.save(image.name, image)
                videos_header.header_image_file_name = filename
                videos_header.save()

            return HttpResponseRedirect(reverse('admin_pages:manage_resources'))

    context = { 'form': form }
    return render(request, 'admin_pages/manage_resources/worship_videos/manage_worship_videos_header.html', context)


@login_required
def new_speaker(request):
    """Provides the user a form template to create a new Speaker object.

    Parameters:
    request (HttpRequest): An HTTP Request object. 

    Returns:
    HttpResponse: Directs the user to the appropriate URL depending on the vaidity of the form.
    """
    if (request.method != 'POST'):
        form = SpeakerForm()
    else:
        form = SpeakerForm(data=request.POST)
        if (form.is_valid()):
            form.save()
            return HttpResponseRedirect(reverse('admin_pages:manage_resources'))

    context = { 'form': form }
    return render(request, 'admin_pages/manage_resources/speakers/new_speaker.html', context)


@login_required
def edit_speaker(request, speaker_id):
    """Provides the user a form template to edit an existing Speaker object.

    Parameters:
    request (HttpRequest): An HTTP Request object. 

    Returns:
    HttpResponse: Directs the user to the appropriate URL depending on the vaidity of the form.
    """
    speaker = Speaker.objects.get(id=speaker_id)

    if(request.method != 'POST'):
        form = SpeakerForm(instance=speaker)
    else:
        form = SpeakerForm(instance=speaker, data=request.POST)
        if (form.is_valid()):
            form.save()
            return HttpResponseRedirect(reverse('admin_pages:manage_resources'))

    context = { 'speaker': speaker, 'form': form }
    return render(request, 'admin_pages/manage_resources/speakers/edit_speaker.html', context)


@login_required
def confirm_delete_speaker(request, speaker_id):
    """Provides the user a form template to confirm whether to delete
    an existing Speaker object or not.

    Parameters:
    request (HttpRequest): An HTTP Request object. 

    Returns:
    HttpResponse: Directs the user to the appropriate URL to display the template.
    """
    speaker = Speaker.objects.get(id=speaker_id)

    context = { 'speaker': speaker }
    return render(request, 'admin_pages/manage_resources/speakers/confirm_delete_speaker.html', context)


@login_required
def delete_speaker(request, speaker_id):
    """Deletes an existing Speaker object.

    Parameters:
    request (HttpRequest): An HTTP Request object.

    Returns:
    HttpResponse: Directs the user to the appropriate URL.
    """
    speaker = Speaker.objects.get(id=speaker_id)
    sermons = Sermon.objects.filter(speaker_id=speaker.id)

    for sermon in sermons:
        try:
            os.remove(os.path.join(SERMONS_AUDIO_DIR, sermon.file_name))
        except:
            pass
    speaker.delete() # Sermons will be automatically deleted as well.

    return HttpResponseRedirect(reverse('admin_pages:manage_resources'))


@login_required
def new_artist(request):
    """Provides the user a form template to create a new Artist object.

    Parameters:
    request (HttpRequest): An HTTP Request object. 
    
    Returns:
    HttpResponse: Directs the user to the appropriate URL depending on the vaidity of the form.
    """
    if (request.method != 'POST'):
        form = ArtistForm()
    else:
        form = ArtistForm(data=request.POST)
        if (form.is_valid()):
            form.save()
            return HttpResponseRedirect(reverse('admin_pages:manage_resources'))

    context = { 'form': form }
    return render(request, 'admin_pages/manage_resources/artists/new_artist.html', context)


@login_required
def edit_artist(request, artist_id):
    """Provides the user a form template to edit an existing Artist object.

    Parameters:
    request (HttpRequest): An HTTP Request object. 

    Returns:
    HttpResponse: Directs the user to the appropriate URL depending on the vaidity of the form.
    """
    artist = Artist.objects.get(id=artist_id)

    if(request.method != 'POST'):
        form = ArtistForm(instance=artist)
    else:
        form = ArtistForm(instance=artist, data=request.POST)
        if (form.is_valid()):
            form.save()
            return HttpResponseRedirect(reverse('admin_pages:manage_resources'))

    context = { 'artist': artist, 'form': form }
    return render(request, 'admin_pages/manage_resources/artists/edit_artist.html', context)


@login_required
def confirm_delete_artist(request, artist_id):
    """Provides the user a form template to confirm whether to delete
    an existing Artist object or not.

    Parameters:
    request (HttpRequest): An HTTP Request object.

    Returns:
    HttpResponse: Directs the user to the appropriate URL.
    """
    artist = Artist.objects.get(id=artist_id)

    context = { 'artist': artist }
    return render(request, 'admin_pages/manage_resources/artists/confirm_delete_artist.html', context)


@login_required
def delete_artist(request, artist_id):
    """Deletes an existing Artist object.

    Parameters:
    request (HttpRequest): An HTTP Request object.

    Returns:
    HttpResponse: Directs the user to the appropriate URL depending on the vaidity of the form.
    """
    artist = Artist.objects.get(id=artist_id)
    songs = Song.objects.filter(artist_id=artist.id)

    for song in songs:
        try:
            os.remove(os.path.join(MUSIC_AUDIO_DIR, song.file_name))
        except:
            pass
    artist.delete() # Automatically deletes Song objects as well.

    return HttpResponseRedirect(reverse('admin_pages:manage_resources'))


@login_required
def new_sermon(request, speaker_id):
    """Provides the user a form template to create a new Sermon object
    and upload the cooresponding audio file (for the Sermons page).

    Parameters:
    request (HttpRequest): An HTTP Request object.
    speaker_id (int): The PK of the Speaker object which will become the FK of the new Sermon object.
    
    Returns:
    HttpResponse: Directs the user to the appropriate URL depending on the vaidity of the form.
    """
    speaker = Speaker.objects.get(id=speaker_id)

    if (request.method != 'POST'):
        form = SermonForm()
    else:
        fs_storage = FileSystemStorage(location=SERMONS_AUDIO_DIR)
        form = SermonForm(data=request.POST, files=request.FILES)

        if (form.is_valid()):
            new_sermon = form.save(commit=False)

            if len(request.FILES) != 0:
                audio = request.FILES['audio_file']
                filename = fs_storage.save(audio.name, audio)

                new_sermon.file_name = str(filename)

            new_sermon.speaker = speaker
            new_sermon.save()
            return HttpResponseRedirect(reverse('admin_pages:manage_resources'))

    context = { 'speaker': speaker, 'form': form }
    return render(request, 'admin_pages/manage_resources/sermons/new_sermon.html', context)


@login_required
def edit_sermon(request, sermon_id):
    """Provides the user a form template to edit an existing Sermon object
    and replace the cooresponding audio file (for the Sermons page).

    Parameters:
    request (HttpRequest): An HTTP Request object.
    sermon_id (int): The PK of the Sermon object to edit.

    Returns:
    HttpResponse: Directs the user to the appropriate URL depending on the vaidity of the form.
    """
    sermon = Sermon.objects.get(id=sermon_id)

    if(request.method != 'POST'):
        form = SermonForm(instance=sermon)
    else:
        fs_storage = FileSystemStorage(location=SERMONS_AUDIO_DIR)
        form = SermonForm(instance=sermon, data=request.POST, files=request.FILES)

        if (form.is_valid()):
            edit_sermon = form.save(commit=False)

            if len(request.FILES) != 0:
                if (sermon.file_name != ''):
                    try:
                        os.remove(os.path.join(SERMONS_AUDIO_DIR, sermon.file_name))
                    except:
                        pass

                audio = request.FILES['audio_file']
                filename = fs_storage.save(audio.name, audio)
                edit_sermon.file_name = str(filename)

            edit_sermon.save()
            return HttpResponseRedirect(reverse('admin_pages:manage_resources'))

    context = { 'sermon': sermon, 'form': form }
    return render(request, 'admin_pages/manage_resources/sermons/edit_sermon.html', context)


@login_required
def delete_sermon(request, sermon_id):
    """Deletes a Sermon object and its cooresponding audio file, if any.

    Parameters:
    request (HttpRequest): An HTTP Request object.
    sermon_id (int): The PK of the Sermon object to delete.

    Returns:
    HttpResponse: Directs the user to the appropriate URL.
    """
    sermon = Sermon.objects.get(id=sermon_id)
    if (sermon.file_name != ''):
        try:
            os.remove(os.path.join(SERMONS_AUDIO_DIR, sermon.file_name))
        except:
            pass
    sermon.delete()
    return HttpResponseRedirect(reverse('admin_pages:manage_resources'))


@login_required
def new_song(request, artist_id):
    """Provides the user a form template to create a new Song object
    and upload the cooresponding audio file (for the Worship Music page).

    Parameters:
    request (HttpRequest): An HTTP Request object.
    artist_id (int): The PK of the Artist object which will become the FK of the new Song object.
    
    Returns:
    HttpResponse: Directs the user to the appropriate URL depending on the vaidity of the form.
    """
    artist = Artist.objects.get(id=artist_id)

    if (request.method != 'POST'):
        form = MusicForm()
    else:
        fs_storage = FileSystemStorage(location=MUSIC_AUDIO_DIR)
        form = MusicForm(data=request.POST, files=request.FILES)

        if (form.is_valid()):
            new_song = form.save(commit=False)

            new_song.file_name = ''

            if len(request.FILES) != 0:
                audio = request.FILES['audio_file']
                filename = fs_storage.save(audio.name, audio)

                new_song.file_name = str(filename)

            new_song.artist = artist
            new_song.save()
            return HttpResponseRedirect(reverse('admin_pages:manage_resources'))

    context = { 'artist': artist, 'form': form }
    return render(request, 'admin_pages/manage_resources/worship_music/new_song.html', context)


@login_required
def edit_song(request, song_id):
    """Provides the user a form template to edit an existing Song object
    and replace the cooresponding audio file (for the Worship Music page).

    Parameters:
    request (HttpRequest): An HTTP Request object.
    sermon_id (int): The PK of the Song object to edit.

    Returns:
    HttpResponse: Directs the user to the appropriate URL depending on the vaidity of the form.
    """
    song = Song.objects.get(id=song_id)

    if(request.method != 'POST'):
        form = MusicForm(instance=song)
    else:
        fs_storage = FileSystemStorage(location=MUSIC_AUDIO_DIR)
        form = MusicForm(instance=song, data=request.POST, files=request.FILES)
        if (form.is_valid()):
            edit_song = form.save(commit=False)

            if len(request.FILES) != 0:
                if (song.file_name != ''):
                    try:
                        os.remove(os.path.join(MUSIC_AUDIO_DIR, song.file_name))
                    except:
                        pass

                audio = request.FILES['audio_file']
                filename = fs_storage.save(audio.name, audio)
                edit_song.file_name = str(filename)

            edit_song.save()
            return HttpResponseRedirect(reverse('admin_pages:manage_resources'))

    context = { 'song': song, 'form': form }
    return render(request, 'admin_pages/manage_resources/worship_music/edit_song.html', context)


@login_required
def delete_song(request, song_id):
    """Deletes a Song object and its cooresponding audio file, if any.

    Parameters:
    request (HttpRequest): An HTTP Request object.
    sermon_id (int): The PK of the Song object to delete.

    Returns:
    HttpResponse: Directs the user to the appropriate URL.
    """
    song = Song.objects.get(id=song_id)
    if (song.file_name != ''):
        try:
            os.remove(os.path.join(MUSIC_AUDIO_DIR, song.file_name))
        except:
            pass
    song.delete()
    return HttpResponseRedirect(reverse('admin_pages:manage_resources'))


@login_required
def new_worship_video(request, speaker_id):
    """Provides the user a form template to create a new WorshipVideo object
    and upload the cooresponding bulletin PDF file (for the Worship Videos page).

    Parameters:
    request (HttpRequest): An HTTP Request object.
    speaker_id (int): The PK of the Speaker object which will become the FK of the new WorshipVideo object.
    
    Returns:
    HttpResponse: Directs the user to the appropriate URL depending on the vaidity of the form.
    """
    speaker = Speaker.objects.get(id=speaker_id)

    if (request.method != 'POST'):
        form = WorshipVideoForm()
    else:
        fs_storage = FileSystemStorage(location=VIDEOS_BULLETINS_DIR)
        form = WorshipVideoForm(data=request.POST, files=request.FILES)

        if (form.is_valid()):
            new_video_form = form.save(commit=False)
            new_video_form.file_name = ''

            if len(request.FILES) != 0:
                bulletin = request.FILES['bulletin_file']            
                filename = fs_storage.save(bulletin.name, bulletin)

                new_video_form.file_name = str(filename)

            iframe = new_video_form.iframe.replace('<iframe', '<iframe class=\"iframe-sm\"')
            new_video_form.iframe = iframe
            new_video_form.speaker = speaker
            new_video_form.save()
            try:
                os.remove(os.path.join(settings.BASE_DIR, filename))
            except:
                pass
            return HttpResponseRedirect(reverse('admin_pages:manage_resources'))

    context = { 'speaker': speaker, 'form': form }
    return render(request, 'admin_pages/manage_resources/worship_videos/new_worship_video.html', context)


def edit_worship_video(request, video_id):
    """Provides the user a form template to edit an existing Worship Video object
    and replace the cooresponding audio file (for the Worship Videos page).

    Parameters:
    request (HttpRequest): An HTTP Request object.
    video_id (int): The PK of the WorshipVideo object to edit.

    Returns:
    HttpResponse: Directs the user to the appropriate URL depending on the vaidity of the form.
    """
    video = WorshipVideo.objects.get(id=video_id)

    if (request.method != 'POST'):
        form = WorshipVideoForm(instance=video)
    else:
        fs_storage = FileSystemStorage(location=VIDEO_BULLETINS_DIR)
        form = WorshipVideoForm(instance=video, data=request.POST, files=request.FILES)

        if (form.is_valid()):
            edit_video = form.save(commit=False)

            if len(request.FILES) != 0:
                if (video.file_name != ''):
                    try:
                        os.remove(os.path.join(VIDEO_BULLETINS_DIR, video.file_name))
                    except:
                        pass
                
                bulletin = request.FILES['bulletin_file']
                filename = fs_storage.save(bulletin.name, bulletin)
                edit_video.file_name = str(filename)
            
            iframe = edit_video.iframe
            if not ('class=\"iframe-sm\"' in iframe):
                iframe = iframe.replace('<iframe', '<iframe class=\"iframe-sm\"')
                edit_video.iframe = iframe
            
            edit_video.save()
            try:
                os.remove(os.path.join(settings.BASE_DIR, filename))
            except:
                pass
            return HttpResponseRedirect(reverse('admin_pages:manage_resources'))

    context = { 'worship_video': video, 'form': form }
    return render(request, 'admin_pages/manage_resources/worship_videos/edit_worship_video.html', context)


@login_required
def delete_worship_video(request, video_id):
    """Deletes a WorshipVideo object and its cooresponding audio file, if any.

    Parameters:
    request (HttpRequest): An HTTP Request object.
    video_id (int): The PK of the WowrshipVideo object to delete.

    Returns:
    HttpResponse: Directs the user to the appropriate URL.
    """
    video = WorshipVideo.objects.get(id=video_id)

    if (video.file_name != ''):
        try:
            os.remove(os.path.join(VIDEO_BULLETINS_DIR, video.file_name))
        except:
            pass
    video.delete()
    return HttpResponseRedirect(reverse('admin_pages:manage_resources'))


@login_required
def manage_services(request):
    """Provides the user a form template to edit the data of the Services
    object (for Services page content) with id 1 and to upload and format
    images for this page.

    Parameters:
    request (HttpRequest): An HTTP Request object. 

    Returns:
    HttpResponse: Directs the user to the appropriate URL depending on the request method.
    """
    services = Services.objects.get(id=1)

    if (request.method != 'POST'):
        form = ServicesForm(instance=services)
    else:
        form = ServicesForm(instance=services, data=request.POST)

        if (form.is_valid()):
            form.save()

            if (services.delete_box1_img):
                services.box1_img_file_name = ''
                try_delete_files(SERVICES_BOX1_IMG_DIR)

            if (services.delete_box2_img):
                services.box2_img_file_name = ''
                try_delete_files(SERVICES_BOX2_IMG_DIR)

            if (services.delete_box3_img):
                services.box3_img_file_name = ''
                try_delete_files(ERVICES_BOX3_IMG_DIR)

            if (len(request.FILES) != 0):
                if('header_image' in request.FILES):
                    try_delete_files(SERVICES_HEADER_DIR)
                    fs_storage = FileSystemStorage(location=SERVICES_HEADER_DIR)
                    image = request.FILES['header_image']
                    filename = fs_storage.save(image.name, image)
                    services.header_image_file_name = filename
                    services.save()

                if ('box1_img' in request.FILES):
                    try_delete_files(SERVICES_BOX1_IMG_DIR) # Try delete here in case delete wasn't specified.
                    fs_storage = FileSystemStorage(location=SERVICES_BOX1_IMG_DIR)
                    image = request.FILES['box1_img']
                    services.box1_img_file_name = image.name
                    fs_storage.save(image.name, image)

                if ('box2_img' in request.FILES):
                    try_delete_files(SERVICES_BOX2_IMG_DIR) # Try delete here in case delete wasn't specified.
                    fs_storage = FileSystemStorage(location=SERVICES_BOX2_IMG_DIR)
                    image = request.FILES['box2_img']
                    services.box2_img_file_name = image.name
                    fs_storage.save(image.name, image)

                if ('box3_img' in request.FILES):
                    try_delete_files(SERVICES_BOX3_IMG_DIR) # Try delete here in case delete wasn't specified.
                    fs_storage = FileSystemStorage(location=SERVICES_BOX3_IMG_DIR)
                    image = request.FILES['box3_img']
                    services.box3_img_file_name = image.name
                    fs_storage.save(image.name, image)

            services.save()

            return HttpResponseRedirect(reverse('admin_pages:admin_index'))

    context = { 'services': services, 'form': form }
    return render(request, 'admin_pages/manage_services/manage_services.html', context)


@login_required
def manage_contact(request):
    """Provides the user a form template to edit the data of the Contact
    object (for Contact page content) with id 1.

    Parameters:
    request (HttpRequest): An HTTP Request object. 

    Returns:
    HttpResponse: Directs the user to the appropriate URL depending on the request method.
    """
    contact = Contact.objects.get(id=1)

    if (request.method != 'POST'):
        form = ContactForm(instance=contact)
    else:
        form = ContactForm(instance=contact, data=request.POST)

        if (form.is_valid()):
            form.save()

            if (len(request.FILES) != 0):
                if('header_image' in request.FILES):
                    try_delete_files(CONTACT_HEADER_DIR)
                    fs_storage = FileSystemStorage(location=CONTACT_HEADER_DIR)
                    image = request.FILES['header_image']
                    filename = fs_storage.save(image.name, image)
                    contact.header_image_file_name = filename
                    contact.save()

            return HttpResponseRedirect(reverse('admin_pages:admin_index'))

    context = { 'contact': contact, 'form': form }
    return render(request, 'admin_pages/manage_contact/manage_contact.html', context)


@login_required
def manage_seo(request):
    """Provides the user a form template to edit the data of the SEO
    object (for--well--SEO) with id 1.

    Parameters:
    request (HttpRequest): An HTTP Request object. 

    Returns:
    HttpResponse: Directs the user to the appropriate URL depending on the request method.
    """
    seo = SEO.objects.get(id=1)

    if(request.method != 'POST'):
        form = SEOForm(instance=seo)
    else:
        form = SEOForm(instance=seo, data=request.POST)

        if (form.is_valid()):
            form.save()

            if len(request.FILES) != 0:
                print("ROBOTS!\n")
                fs_storage = FileSystemStorage(location=ROBOTS_TXT_DIR)
                try:
                    os.remove(os.path.join(ROBOTS_TXT_DIR, 'robots.txt'))
                except:
                    pass
                robots_file = request.FILES['robots_txt']
                fs_storage.save('robots.txt', robots_file)

            return HttpResponseRedirect(reverse('admin_pages:admin_index'))

    context = { 'seo': seo, 'form': form }
    return render(request, 'admin_pages/manage_seo/manage_seo.html', context)


@login_required
def manage_users(request):
    """Provides the user a form template to facilitate creation and deletion of a
    User admin (ish) account. The user is considered an admin for access to the 
    Admin Pages and API but is not a true Django admin which is unneccessary since
    there are no admin-registered models.

    Parameters:
    request (HttpRequest): An HTTP Request object. 

    Returns:
    HttpResponse: Directs the user to the appropriate URL.
    """
    users = User.objects.all()

    context = { 'users': users }
    return render(request, 'admin_pages/manage_users/manage_users.html', context)


@login_required
def manage_email_account(request):
    """Provides the user a form template to edit the EmailAccount object
    with id 1. The object's single email_addr field will contain the
    email address of the recipient for site_pages.form_sender which will
    send form data as an email.

    Parameters:
    request (HttpRequest): An HTTP Request object. 

    Returns:
    HttpResponse: Directs the user to the appropriate URL depending on the request method.
    """
    email_account = EmailAccount.objects.get(id=1)

    if (request.method != 'POST'):
        form = EmailAccountForm(instance=email_account)
    else:
        form = EmailAccountForm(instance=email_account, data=request.POST)
        
        if (form.is_valid()):
            form.save()
            form_sender.refresh_email_recipient()
            return HttpResponseRedirect(reverse('admin_pages:admin_index'))

    context = { 'email_account': email_account, 'form': form }
    return render(request, 'admin_pages/manage_email/manage_email.html', context)


@login_required
def manage_ip_nolog_list(request):
    """Provides the user a template to control the contents of the list of IP
    addresses which site_pages.db_logger will ignore when logging a page view
    or unique visit from one such address. Allows CRUD operations for the
    NoLogIPModel objects.

    Parameters:
    request (HttpRequest): An HTTP Request object. 

    Returns:
    HttpResponse: Directs the user to the appropriate URL.
    """
    nolog_ips = NoLogIPModel.objects.all()

    context = { 'nolog_ips': nolog_ips }
    return render(request, 'admin_pages/manage_denylists/manage_ip_denylist.html', 
                    context)


@login_required
def new_nolog_ip(request):
    """Provides the user a form template to create a new NoLogIPModel object.

    Parameters:
    request (HttpRequest): An HTTP Request object. 
    
    Returns:
    HttpResponse: Directs the user to the appropriate URL depending on the vaidity of the form.
    """
    if (request.method != 'POST'):
        form = NoLogIPForm()
    else:
        form = NoLogIPForm(data=request.POST)
        if(form.is_valid()):
            form.save()
            site_views.refresh_nolog_ip_list() # Get db_logger to update the list.
            return HttpResponseRedirect(reverse(
                'admin_pages:manage_ip_nolog_list'))

    context = { 'form': form }
    return render(request, 'admin_pages/manage_denylists/nologips/new_nologip.html',
                    context)


@login_required
def edit_nolog_ip(request, nologip_id):
    """Provides the user a form template to edit an existing NoLogIPModel object.

    Parameters:
    request (HttpRequest): An HTTP Request object. 

    Returns:
    HttpResponse: Directs the user to the appropriate URL depending on the vaidity of the form.
    """
    nolog_ip = NoLogIPModel.objects.get(id=nologip_id)

    if(request.method != 'POST'):
        form = NoLogIPForm(instance=nolog_ip)
    else:
        form = NoLogIPForm(instance=nolog_ip, data=request.POST)
        if (form.is_valid()):
            form.save()
            site_views.refresh_nolog_ip_list()
            return HttpResponseRedirect(reverse(
                    'admin_pages:manage_ip_nolog_list'
                ))

    context = { 'nolog_ip': nolog_ip, 'form': form }
    return render(request, 'admin_pages/manage_denylists/nologips/edit_nologip.html', 
                    context)


@login_required
def delete_nolog_ip(request, nologip_id):
    """Deletes an existing NoLogIPModel object.

    Parameters:
    request (HttpRequest): An HTTP Request object.
    nologip_id (int): The PK of the NoLogIPModel object to delete.

    Returns:
    HttpResponse: Directs the user to the appropriate URL.
    """
    NoLogIPModel.objects.get(id=nologip_id).delete()
    site_views.refresh_nolog_ip_list()
    return HttpResponseRedirect(reverse('admin_pages:manage_ip_nolog_list'))


@login_required
def manage_email_denylist(request):
    """Provides the user a template to control the contents of the list of
    email addresses which site_pages.views will check against an email address
    in a submitted form before emailing that form data to the recipient address
    such that if the address is listed, the form data will not be emailed.
    Allows CRUD operations for the DenylistEmailModel objects.

    Parameters:
    request (HttpRequest): An HTTP Request object. 

    Returns:
    HttpResponse: Directs the user to the appropriate URL.
    """
    denylist_emails = DenylistEmailModel.objects.all()

    context = { 'denylist_emails': denylist_emails }
    return render(request, 'admin_pages/manage_denylists/manage_email_denylist.html', 
                    context)


def new_denylistemail(request):
    """Provides the user a form template to create a new DenylistEmailModel object.

    Parameters:
    request (HttpRequest): An HTTP Request object. 
    
    Returns:
    HttpResponse: Directs the user to the appropriate URL depending on the vaidity of the form.
    """
    if (request.method != 'POST'):
        form = DenylistEmailForm()
    else:
        form = DenylistEmailForm(data=request.POST)
        if (form.is_valid()):
            form.save()
            site_views.refresh_email_denylist()
            return HttpResponseRedirect(reverse(
                'admin_pages:manage_email_denylist'))
    
    context = { 'form': form }
    return render(request, 'admin_pages/manage_denylists/denylistemails/new_denylistemail.html',
                context)


def edit_denylistemail(request, denylistemail_id):
    """Provides the user a form template to edit an existing DenylistEmailModel object.

    Parameters:
    request (HttpRequest): An HTTP Request object. 

    Returns:
    HttpResponse: Directs the user to the appropriate URL depending on the vaidity of the form.
    """
    denylistemail = DenylistEmailModel.objects.get(id=denylistemail_id)

    if (request.method != 'POST'):
        form = DenylistEmailForm(instance=denylistemail)
    else:
        form = DenylistEmailForm(instance=denylistemail, data=request.POST)
        if (form.is_valid()):
            form.save()
            site_views.refresh_email_denylist()
            return HttpResponseRedirect(reverse(
                'admin_pages:manage_email_denylist'
            ))
    
    context = { 'denylistemail': denylistemail, 'form': form }
    return render(request, 'admin_pages/manage_denylists/denylistemails/edit_denylistemail.html',
                    context)


def delete_denylistemail(request, denylistemail_id):
    """Deletes an existing DenylistEmailModel object.

    Parameters:
    request (HttpRequest): An HTTP Request object.
    denylistemail_id (int): The PK of the DenylistEmailModel object to delete.

    Returns:
    HttpResponse: Directs the user to the appropriate URL.
    """
    DenylistEmailModel.objects.get(id=denylistemail_id).delete()
    site_views.refresh_email_denylist()
    return HttpResponseRedirect(reverse('admin_pages:manage_email_denylist'))