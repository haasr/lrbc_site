from admin_pages.models import SiteLook, Home, About, LeadershipHeader, Services, Contact, SermonsHeader, MusicHeader, VideosHeader, SEO, EmailAccount
from django.contrib.auth.models import User
from lrbc_site import settings
import os

SITE_PAGES_DIR = settings.BASE_DIR + '/static/site_pages/'
DEFAULT_FONT = '<link href="https://fonts.googleapis.com/css2?family=Mulish&display=swap" rel="stylesheet">&&Mulish'

try:
    os.mkdir(SITE_PAGES_DIR + 'home/gallery_images/')
except:
    pass
try:
    os.mkdir(SITE_PAGES_DIR + 'about/gallery_images/')
except:
    pass
try:
    os.mkdir(SITE_PAGES_DIR + 'about/box1_image/')
except:
    pass
try:
    os.mkdir(SITE_PAGES_DIR + 'about/box2_image/')
except:
    pass
try:
    os.mkdir(SITE_PAGES_DIR + 'leadership')
except:
    pass
try:
    os.mkdir(SITE_PAGES_DIR + 'leadership/header_image')
except:
    pass
try:
    os.mkdir(SITE_PAGES_DIR + 'leadership/leaders_images')
except:
    pass
try:
    os.mkdir(SITE_PAGES_DIR + 'resources/sermons/audio/')
except:
    pass
try:
    os.mkdir(SITE_PAGES_DIR + 'resources/worship_music/audio/')
except:
    pass
try:
    os.mkdir(SITE_PAGES_DIR + 'resources/worship_videos/bulletins/')
except:
    pass

x = SiteLook(
    id=1,
    show_home=False,
    show_about=True,
    show_sermons=True,
    show_music=True,
    show_videos=True,
    show_services=True,
    show_contact=True,
    font=DEFAULT_FONT,
    footer_tagline='A church for the community',
    footer_about='Our church is dedicated to helping our commmunity impacting the world.',
    footer_location='',
    footer_contact_phone='',
    footer_contact_email='',
    show_email_form=False,
    lat='',
    lon=''
)
x.save()

x = Home(
    id=1, 
    alert_banner='',
    tagline='',
    tagline_size='h1',
    tagline_color='#FFFFFF',
    email_addr='',
    facebook_link='',
    twitter_link='',
    instagram_link='', 
    youtube_link='',
    about_label='', 
    live_link='',
    static_gallery=False,
    delete_gallery=False,
)
x.save()

x = About(
    id=1,
    show_header_image=True,
    header_image_file_name='about.png',
    header_text='',
    box1_header_text='',
    box1_content_text='',
    box1_img_file_name='',
    box2_header_text='',
    box2_content_text='',
    box2_img_file_name='',
    static_gallery=False,
    delete_gallery=False,
    delete_box1_img=False,
    delete_box2_img=False
)
x.save()

x = LeadershipHeader(
    id=1,
    show_header_image=True,
    header_image_file_name='',
    header_text='',
    description_text=''
)
x.save()

x = Services(
    id=1,
    show_header_image=True,
    header_image_file_name='services.png',
    box1_header_text='',
    box1_content_text='',
    box1_img_file_name='',
    delete_box1_img=False,
    box1_link='',
    box1_link_desc='',
    box2_header_text='',
    box2_content_text='',
    box2_img_file_name='',
    delete_box2_img=False,
    box2_link='',
    box2_link_desc='',
    box3_header_text='',
    box3_content_text='',
    box3_img_file_name='',
    delete_box3_img=False,
    box3_link=False,
    box3_link_desc=False,
    show_prayer_form=False
)
x.save()

x = Contact(
    id=1,
    show_header_image=True,
    header_image_file_name='contact.png',
    phone_fax_header_text='',
    contact_phone='',
    contact_fax='',
    addr_mail_header_text='',
    contact_address='',
    contact_mailbox='',
    contact_email_addr='',
    show_contact_form=False
)
x.save()

x = SermonsHeader(
    id=1,
    show_header_image=True,
    header_image_file_name='sermons.png',
    header_text=''
)
x.save()

x = MusicHeader(
    id=1,
    show_header_image=True,
    header_image_file_name='worship_music.png',
    header_text=''
)
x.save()

x = VideosHeader(
    id=1,
    show_header_image=True,
    header_image_file_name='worship_videos.jpg',
    header_text=''
)
x.save()

x = SEO(
    id=1,
    meta_title='',
    meta_description='',
    meta_keywords='',
    meta_author='',
    robots_index=True,
    robots_follow=True
)
x.save()

x = EmailAccount(
    id=1,
    email_addr=''
)
x.save()

print('\n###### Create initial admin account ######')
print('You must create an initial admin account\nto log into <hostname>/users/login/\n')
fname = input('  First Name: ')
lname = input('  Last Name:  ')
mail  = input('  Email:      ')
uname = input('  Username:   ')
pswd  = input('  Password:   ')

new_usr = User.objects.create_user(first_name=fname, last_name=lname, email=mail,
                                    username=uname, password=pswd)
new_usr.save()
