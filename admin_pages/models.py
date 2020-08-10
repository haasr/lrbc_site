from django.db import models
from django.contrib.auth.models import User
from colorfield.fields import ColorField


class SiteLook(models.Model):
    """Contains attributes that determine the content of the nav and footer."""
    show_home      = models.BooleanField(default=False)
    show_about     = models.BooleanField(default=True)
    show_sermons   = models.BooleanField(default=True)
    show_music     = models.BooleanField(default=True)
    show_videos    = models.BooleanField(default=True)
    show_services  = models.BooleanField(default=True)
    show_contact   = models.BooleanField(default=True)

    footer_tagline       = models.CharField(max_length=26)
    footer_about         = models.CharField(max_length=300)
    footer_location      = models.CharField(max_length=800)
    footer_contact_phone = models.CharField(max_length=21)
    footer_contact_email = models.CharField(max_length=320)
    show_email_form      = models.BooleanField(default=True)

    favicon        = models.FileField()
    navigation_img = models.FileField()

    footer_text_color = models.CharField(max_length=10)

    footer_color  = ColorField(default='#B0D5D1')
    gallery_color = ColorField(default='#B5E0E0')

    # Future TODO:
    # When form submitted have view make API call to convert
    # address to latitude and longitude. This way you can
    # create a Google Maps iframe to go in the footer.
    lat = models.CharField(max_length=200)
    lon = models.CharField(max_length=200)


class Home(models.Model):
    """Contains attributes that determine the content of the home page."""
    alert_banner   = models.CharField(max_length=300, blank=True, null=True)
    tagline        = models.CharField(max_length=100, blank=True, null=True)
    tagline_size   = models.CharField(max_length=2) # Use h1, h2, or h3 as options.
    tagline_color  = ColorField(default='#FFFFFF')
    email_addr     = models.CharField(max_length=320, blank=True, null=True)
    # Max lengths determined by https:// scheme +
    # host_name/ + filepath (if any) + max length of username.
    facebook_link  = models.CharField(max_length=75, blank=True, null=True)
    twitter_link   = models.CharField(max_length=35, blank=True, null=True)
    instagram_link = models.CharField(max_length=56, blank=True, null=True)
    youtube_link   = models.CharField(max_length=49, blank=True, null=True)

    # These lengths are arbitrary ( there really shouldn't
    # be a longer URL though).
    about_label    = models.CharField(max_length=200, blank=True, null=True)
    live_link      = models.CharField(max_length=200, blank=True, null=True)

    background_img = models.FileField()
    gallery_imgs   = models.FileField()
    static_gallery = models.BooleanField(default=False)
    delete_gallery = models.BooleanField(default=False)


class About(models.Model):
    """Contains attributes that determine the content of the about page."""
    show_header_image      = models.BooleanField(default=True)
    header_image           = models.FileField()
    header_image_file_name = models.TextField()

    box1_header_text   = models.CharField(max_length=75, blank=True, null=True)
    box1_content_text  = models.CharField(max_length=6000, blank=True, null=True)
    box1_img           = models.FileField()
    box1_img_alt       = models.CharField(max_length=75)
    box1_img_size      = models.CharField(max_length=12, blank=True, null=True)
    box1_img_position  = models.CharField(max_length=22, blank=True, null=True)
    box1_img_file_name = models.TextField()

    box2_header_text   = models.CharField(max_length=75, blank=True, null=True)
    box2_content_text  = models.CharField(max_length=6000, blank=True, null=True)
    box2_img           = models.FileField()
    box2_img_alt       = models.CharField(max_length=75)
    box2_img_size      = models.CharField(max_length=12, blank=True, null=True)
    box2_img_position  = models.CharField(max_length=22, blank=True, null=True)
    box2_img_file_name = models.TextField()

    gallery_imgs   = models.FileField()
    static_gallery = models.BooleanField(default=False)
    delete_gallery = models.BooleanField(default=False)

    delete_box1_img = models.BooleanField(default=False)
    delete_box2_img = models.BooleanField(default=False)


class Services(models.Model):
    """Contains attributes that determine the content of the services page."""
    show_header_image      = models.BooleanField(default=True)
    header_image           = models.FileField()
    header_image_file_name = models.TextField()

    box1_header_text   = models.CharField(max_length=75, blank=True, null=True)
    box1_content_text  = models.CharField(max_length=6000, blank=True, null=True)
    box1_img           = models.FileField()
    box1_img_alt       = models.CharField(max_length=75)
    box1_img_size      = models.CharField(max_length=12, blank=True, null=True)
    box1_img_position  = models.CharField(max_length=22, blank=True, null=True)
    box1_img_file_name = models.TextField()
    delete_box1_img    = models.BooleanField(default=False)
    box1_link          = models.CharField(max_length=500, blank=True, null=True)
    box1_link_desc     = models.CharField(max_length=50, blank=True, null=True)

    box2_header_text   = models.CharField(max_length=75, blank=True, null=True)
    box2_content_text  = models.CharField(max_length=6000, blank=True, null=True)
    box2_img           = models.FileField()
    box2_img_alt       = models.CharField(max_length=75)
    box2_img_size      = models.CharField(max_length=12, blank=True, null=True)
    box2_img_position  = models.CharField(max_length=22, blank=True, null=True)
    box2_img_file_name = models.TextField()
    delete_box2_img    = models.BooleanField(default=False)
    box2_link          = models.CharField(max_length=500, blank=True, null=True)
    box2_link_desc     = models.CharField(max_length=50, blank=True, null=True)

    box3_header_text   = models.CharField(max_length=75, blank=True, null=True)
    box3_content_text  = models.CharField(max_length=6000, blank=True, null=True)
    box3_img           = models.FileField()
    box3_img_alt       = models.CharField(max_length=75)
    box3_img_size      = models.CharField(max_length=12, blank=True, null=True)
    box3_img_position  = models.CharField(max_length=22, blank=True, null=True)
    box3_img_file_name = models.TextField()
    delete_box3_img    = models.BooleanField(default=False)
    box3_link          = models.CharField(max_length=500, blank=True, null=True)
    box3_link_desc     = models.CharField(max_length=50, blank=True, null=True)

    show_prayer_form = models.BooleanField(default=False)


class Contact(models.Model):
    """Contains attributes that determine the content of the contact page."""
    show_header_image      = models.BooleanField(default=True)
    header_image           = models.FileField()
    header_image_file_name = models.TextField()

    phone_fax_header_text = models.CharField(max_length=75, blank=True, null=True)
    contact_phone         = models.CharField(max_length=21, blank=True, null=True)
    contact_fax           = models.CharField(max_length=21, blank=True, null=True)

    addr_mail_header_text = models.CharField(max_length=75, blank=True, null=True)
    contact_address       = models.CharField(max_length=900, blank=True, null=True)
    contact_mailbox       = models.CharField(max_length=900, blank=True, null=True)

    contact_email_addr = models.CharField(max_length=320, blank=True, null=True)

    show_contact_form = models.BooleanField(default=True)


class SermonsHeader(models.Model):
    """Contains attributes that determine the header content of the Sermons page."""
    show_header_image = models.BooleanField(default=True)
    header_image      = models.FileField()
    header_text       = models.CharField(max_length=75)

    header_image_file_name = models.TextField()


class MusicHeader(models.Model):
    """Contains attributes that determine the header content of the Worship Music page."""
    show_header_image = models.BooleanField(default=True)
    header_image      = models.FileField()
    header_text       = models.CharField(max_length=75)

    header_image_file_name = models.TextField()


class VideosHeader(models.Model):
    """Contains attributes that determine the header content of the Worship Videos page."""
    show_header_image = models.BooleanField(default=True)
    header_image      = models.FileField()
    header_text       = models.CharField(max_length=75)

    header_image_file_name = models.TextField()


class Speaker(models.Model):
    """Contains attributes that determine a speaker who will have 1:M relationship to Sermons and WorshipVideos."""
    name = models.CharField(max_length=75, blank=False, null=False)

    class Meta:
        verbose_name_plural = 'speakers'


class Artist(models.Model):
    """Contains attributes that determine an artist who will have 1:M relationship to Songs."""
    name = models.CharField(max_length=75, blank=False, null=False)

    class Meta:
        verbose_name_plural = 'artists'


class Sermon(models.Model):
    """Defines the metadata associated with sermon audio file to enable list sorting/filtering."""
    audio_file = models.FileField()
    speaker    = models.ForeignKey(Speaker, on_delete=models.CASCADE)
    title      = models.CharField(max_length=200)
    date       = models.DateField(auto_now=False, auto_now_add=False)
    file_name  = models.TextField()

    class Meta:
        verbose_name_plural = 'sermons'


class Song(models.Model):
    """Defines the metadata associated with music audio file to enable list sorting/filtering."""
    audio_file = models.FileField()
    artist     = models.ForeignKey(Artist, on_delete=models.CASCADE)
    title      = models.CharField(max_length=200)
    date       = models.DateField(auto_now=False, auto_now_add=False)
    file_name  = models.TextField()

    class Meta:
        verbose_name_plural = 'songs'


class WorshipVideo(models.Model):
    """Defines the metadata associated with worship service video to enable list sorting/filtering."""
    iframe        = models.CharField(max_length=500)
    speaker       = models.ForeignKey(Speaker, on_delete=models.CASCADE)
    title         = models.CharField(max_length=200)
    date          = models.DateField(auto_now=False, auto_now_add=False)
    description   = models.CharField(max_length=320)
    bulletin_file = models.FileField()
    file_name     = models.TextField()

    class Meta:
        verbose_name_plural = 'worship_videos'


class SEO(models.Model):
    """Contains attributes that determine meta information for SEO."""
    meta_title       = models.CharField(max_length=100)
    meta_description = models.CharField(max_length=160)
    meta_keywords    = models.CharField(max_length=3000)
    meta_author      = models.CharField(max_length=100)

    robots_index  = models.BooleanField(default=True)
    robots_follow = models.BooleanField(default=True)
    robots_txt    = models.FileField()


class NoLogIPModel(models.Model):
    """Contains attributes to represent an IP address for which no requests made from this address should be logged."""
    ip      = models.CharField(max_length=35, blank=False, null=False)
    comment = models.CharField(max_length=75, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'nologips'


class DenylistEmailModel(models.Model):
    """Contains attributes to represent an email address for which no forms submitted with this address should be emailed."""
    email_addr = models.CharField(max_length=320, blank=False, null=False)
    comment    = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'denylistemails'


class EmailAccount(models.Model):
    """Contains the email address for which form data should be sent to."""
    email_addr = models.CharField(max_length=320, blank=False, null=False)