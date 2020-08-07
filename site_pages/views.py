from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from admin_pages.models import *
from .forms import *
from .db_logger import DBLogger
from . import form_sender
from lrbc_site import settings
from datetime import datetime as dt, timedelta

import threading
import os

HOME_GALLERY_IMGS_DIR = settings.STATICFILES_DIRS[0] + '/site_pages/home/gallery_images/'
ABOUT_GALLERY_IMGS_DIR = settings.STATICFILES_DIRS[0] + '/site_pages/about/gallery_images/'
TZ_DELTA = timedelta(hours=-4) # dt.now() in venv is 4 hours ahead of system time!

email_denylist = DenylistEmailModel.objects.all().values_list('email_addr', flat=True)
dblogger = DBLogger()
form_sender.refresh_email_recipient() # Initially populate the recipient.

sitelook = SiteLook.objects.get(id=1)


def refresh_nolog_ip_list():
    """Calls the DBLogger instance's refresh_nolog_ip_list function to
    update a flattened list of the IP addresses of all NoLogIPModel objects
    to use for matching IP addresses.
    """
    t = threading.Thread(target=dblogger.refresh_nolog_ip_list)
    t.start()


def refresh_email_denylist():
    """Updates a flattened list of email addresses of all DenyListEmailModel
    objects to use for matching email addresses in submitted form data.
    """
    global email_denylist
    email_denylist = DenylistEmailModel.objects.all().values_list('email_addr', flat=True)


def process_cookie(request, current_page):
    """
    Each time a page is requested from a viewer, the view function which receives
    the request passes the request reference and a string containing the page name requested
    to this function. The function reads the User-Agent IP address of the request and
    sends the page name passed, the User-Agent, the IP address, and a timestamp string of 
    the occurrence in the form '%Y-%m-%d %H:%M%:%S' (see the datetime documentation).
    Additionally if there is no 'req_time' cookie, the function calls on db_logger's
    log_visitor function passing it the IP, User-Agent, and timestamp string and the
    timestamp string is returned.

    Parameters:
    request (HttpRequest): An HTTP Request object received from the view function will have called this function.
    current_page (str): The page name for which the request is for so that the DBLogger instance may use this for logging.

    Returns: 
    now_str (str): The timestamp string is returned back to the calling function which will use it to set the responses 'req_time' cookie.
    """
    now = dt.now().replace(microsecond=0) # Discard microseconds.
    now = now + TZ_DELTA # Put into EST since venv is 4 hours ahead...
    now_str = now.__str__()

    user_agent = str(request.META.get('HTTP_USER_AGENT'))
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if (x_forwarded_for):
        ip_addr = x_forwarded_for.split(',')[0]
    else:
        ip_addr = request.META.get('REMOTE_ADDR')

    thread1 = threading.Thread(
        target=dblogger.log_page,
        args=(ip_addr, user_agent, current_page, now_str)
    )
    thread1.start()
    
    if not (request.COOKIES.get('req_time')): # New cookie
        thread2 = threading.Thread(
            target=dblogger.log_visitor,
            args=(ip_addr, user_agent, now_str)
        )
        thread2.start()

    return now_str


def send_form(email):
    """Checks the email denylist to see if the string received in the
    email param matches any email address in the list.
    
    Parameters:
    email (str): An email address.

    Returns:
    send (bool): True if the arg received did not match any item in the list and False otherwise.
    """
    send = True
    for email_addr in email_denylist:
        if (email_addr==email):
            send = False
            break
    return send


def submit_contact_email(request):
    """If the form was submitted as a POST request
    and the email in the form data is not on the
    email denylist, the form data is passed to
    the form_sender module's send_contact_form
    function to email the data to the recipient
    specified by the admin_pages.models.EmailAccount
    object with id 1.

    Parameters:
    request (HttpRequest): An HTTP Request object. 

    Returns:
    HttpResponse: Returns the status which will Ajax will use to display a Javascript alert.
    """
    if (request.method == 'POST'):
        now = dt.now() + TZ_DELTA
        now_str = dt.strftime(now, '%m/%d/%y %I:%M %p')
        email = request.POST.get('viewer_email')
        if(send_form(email)):
            t = threading.Thread(target='form_sender.send_contact_email',
                                args=(now_str, email,))
            t.start()
        return HttpResponse(status=200) # Return a 200 even if the email addr is blocked.
    else:
        return HttpResponse(status=403)


def submit_prayer_request(request):
    """If the form was submitted as a POST request,
    the form data is passed to the form_sender module's
    send_cprayer_request function to email the data to the 
    recipient specified by the admin_pages.models.EmailAccount
    object with id 1.

    Parameters:
    request (HttpRequest): An HTTP Request object. 

    Returns
    HttpResponse: Returns the status which will Ajax will use to display a Javascript alert.
    """
    if(request.method == 'POST'):
        now = dt.now() + TZ_DELTA
        now_str = dt.strftime(now, '%m/%d/%y %I:%M %p')
        t = threading.Thread(target=form_sender.send_prayer_request,
                            args=(now_str, request.POST['name'], request.POST['comment'],))
        t.start()
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=403)

    return render(request, 'site_pages/services.html', None)


def sumbit_contact_form(request):
    """If the form was submitted as a POST request
    and the email in the form data is not on the
    email denylist, the form data is passed to
    the form_sender module's send_contact_form
    function to email the data to the recipient
    specified by the admin_pages.models.EmailAccount
    object with id 1.

    Parameters:
    request (HttpRequest): An HTTP Request object. 

    Returns:
    HttpResponse: Returns the status which will Ajax will use to display a Javascript alert.
    """
    if (request.method == 'POST'):
        now = dt.now() + TZ_DELTA
        now_str = dt.strftime(now, '%m/%d/%y %I:%M %p')
        email = request.POST.get('email')
        if (send_form(email)):
            name = (request.POST['fname'] + ' ' + 
                    request.POST['lname'])

            t = threading.Thread(target=form_sender.send_contact_form,
                                args=(now_str, name, email, request.POST.get('comment'),))
            t.start()
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=403)


def index(request):
    """Displays the landing page.

    Parameters:
    request (HttpRequest): An HTTP Request object. 

    Returns:
    HttpResponse: Directs the user to the landing page.
    """
    home = Home.objects.get(id=1)
    gallery_files = os.listdir(HOME_GALLERY_IMGS_DIR)

    display_gallery = True
    if (len(gallery_files) == 0):
        display_gallery = False

    context = { 'home': home, 'gallery_files': gallery_files, 
                'display_gallery': display_gallery }
    response = render(request, 'site_pages/index.html', context)
    req_time = process_cookie(request, 'Index')
    response.set_cookie('req_time', req_time)
    return response


def about(request):
    """Displays the About page if the SiteLook object's boolean,
    show_about is true; redirects the user back to the index page
    otherwise.

    Parameters:
    request (HttpRequest): An HTTP Request object. 

    Returns:
    HttpResponse: Directs the user to the About page.
    """
    sitelook.refresh_from_db()
    if (sitelook.show_about):
        about = About.objects.get(id=1)
        gallery_files = os.listdir(ABOUT_GALLERY_IMGS_DIR)

        header_image = ('/static/site_pages/about/header_image/'
                        + about.header_image_file_name)

        display_gallery = True
        if (len(gallery_files) == 0):
            display_gallery = False

        context = { 'about': about,
                    'header_image': header_image,
                    'gallery_files': gallery_files,
                    'display_gallery': display_gallery }
        response = render(request, 'site_pages/about.html', context)
        req_time = process_cookie(request, 'About')
        response.set_cookie('req_time', req_time)
        return response
    else:
        return HttpResponseRedirect(reverse('index'))


def sermons(request):
    """Displays the Sermons page if the SiteLook object's boolean,
    show_sermons is true; redirects the user back to the index page
    otherwise.

    Parameters:
    request (HttpRequest): An HTTP Request object. 

    Returns:
    HttpResponse: Directs the user to the Sermons page.
    """
    sitelook.refresh_from_db()
    if (sitelook.show_sermons):
        sermons_header = SermonsHeader.objects.get(id=1)
        sermons = Sermon.objects.all().order_by('-date')

        header_image = ('/static/site_pages/resources/sermons/header_image/'
                        + sermons_header.header_image_file_name)

        context = { 
            'header_image': header_image,
            'sermons_header': sermons_header,
            'sermons': sermons
        }
        response = render(request, 'site_pages/sermons.html', context)
        req_time = process_cookie(request, 'Sermons')
        response.set_cookie('req_time', req_time)
        return response
    else:
        return HttpResponseRedirect(reverse('index'))


def worship_music(request):
    """Displays the Worship Music page if the SiteLook object's boolean,
    show_music is true; redirects the user back to the index page
    otherwise.

    Parameters:
    request (HttpRequest): An HTTP Request object. 

    Returns:
    HttpResponse: Directs the user to the Worship Music page.
    """
    sitelook.refresh_from_db()
    if (sitelook.show_music):
        music_header = MusicHeader.objects.get(id=1)
        songs = Song.objects.all().order_by('-date')

        header_image = ('/static/site_pages/resources/worship_music/header_image/'
                        + music_header.header_image_file_name)

        context = { 
            'header_image': header_image,
            'music_header': music_header,
            'songs': songs 
        }
        response = render(request, 'site_pages/worship_music.html', context)
        req_time = process_cookie(request, 'Worship Music')
        response.set_cookie('req_time', req_time)
        return response
    else:
        return HttpResponseRedirect(reverse('index'))


def worship_videos(request):
    """Displays the Worship Videos page if the SiteLook object's boolean,
    show_videos is true; redirects the user back to the index page
    otherwise.

    Parameters:
    request (HttpRequest): An HTTP Request object. 

    Returns:
    HttpResponse: Directs the user to the Worship Videos page.
    """
    sitelook.refresh_from_db()
    if (sitelook.show_videos):
        videos_header = VideosHeader.objects.get(id=1)
        worship_videos = WorshipVideo.objects.all().order_by('-date')
        try:
            initial_iframe = worship_videos[0].iframe.replace('<iframe class=\"iframe-sm\"', 
                                                                '<iframe class=\"iframe-lg\"')
        except:
            initial_iframe = ''

        header_image = ('/static/site_pages/resources/worship_videos/header_image/'
                        + videos_header.header_image_file_name)

        try:
            context = { 
                'header_image': header_image,
                'videos_header': videos_header,
                'videos': worship_videos,
                'initial_video': worship_videos[0],
                'initial_iframe': initial_iframe
            }
        except:
            context = {
                'header_image': header_image,
                'videos_header': videos_header,
                'videos': worship_videos,
                'initial_video': '',
                'initial_iframe': initial_iframe
            }
        response = render(request, 'site_pages/worship_videos.html', context)
        req_time = process_cookie(request, 'Worship Videos')
        response.set_cookie('req_time', req_time)
        return response
    else:
        return HttpResponseRedirect(reverse('index'))


def services(request):
    """Displays the Services page if the SiteLook object's boolean,
    show_services is true; redirects the user back to the index page
    otherwise.

    Parameters:
    request (HttpRequest): An HTTP Request object. 

    Returns:
    HttpResponse: Directs the user to the Services page.
    """
    sitelook.refresh_from_db()
    if (sitelook.show_services):
        services = Services.objects.get(id=1)

        header_image = ('/static/site_pages/services/header_image/'
                        + services.header_image_file_name)

        context = { 'header_image': header_image, 'services': services }
        response = render(request, 'site_pages/services.html', context)
        req_time = process_cookie(request, 'Services')
        response.set_cookie('req_time', req_time)
        return response
    else:
        return HttpResponseRedirect(reverse('index'))


def contact(request):
    """Displays the Contact page if the SiteLook object's boolean,
    show_contact is true; redirects the user back to the index page
    otherwise.

    Parameters:
    request (HttpRequest): An HTTP Request object. 

    Returns:
    HttpResponse: Directs the user to the Contact page.
    """
    sitelook.refresh_from_db()
    if (sitelook.show_contact):
        contact = Contact.objects.get(id=1)

        header_image = ('/static/site_pages/contact/header_image/'
                        + contact.header_image_file_name)

        context = { 'header_image': header_image, 'contact': contact }
        response = render(request, 'site_pages/contact.html', context)
        req_time = process_cookie(request, 'Contact')
        response.set_cookie('req_time', req_time)
        return response
    else:
        return HttpResponseRedirect(reverse('index'))