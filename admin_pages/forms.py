from django import forms
from .models import *
from colorfield.fields import ColorField


class FontOptions:
    GOOGLE_FONTS = (
        ("""<link href="https://fonts.googleapis.com/css2?family=Sansita+Swashed&display=swap" rel="stylesheet">&&Sansita Swashed""", """Sansita Swashed"""),
        ("""<link href="https://fonts.googleapis.com/css2?family=Arimo&display=swap" rel="stylesheet">&&Arimo""", """Arimo"""),
        ("""<link href="https://fonts.googleapis.com/css2?family=Didact+Gothic&display=swap" rel="stylesheet">&&Didact Gothic""", """Didact Gothic"""),
        ("""<link href="https://fonts.googleapis.com/css2?family=Poppins&display=swap" rel="stylesheet">&&Poppins""", """Poppins"""),
        ("""<link href="https://fonts.googleapis.com/css2?family=Roboto&display=swap" rel="stylesheet">&&Roboto""", """Roboto"""),
        ("""<link href="https://fonts.googleapis.com/css2?family=Metrophobic&display=swap" rel="stylesheet">&&Metrophobic""", """Metrophobic"""),
        ("""<link href="https://fonts.googleapis.com/css2?family=Montserrat&display=swap" rel="stylesheet">&&Montserrat""", """Montserrat"""),
        ("""<link href="https://fonts.googleapis.com/css2?family=Mulish&display=swap" rel="stylesheet">&&Mulish""", """Mulish"""),
        ("""<link href="https://fonts.googleapis.com/css2?family=Open+Sans&display=swap" rel="stylesheet">&&Open Sans""", """Open Sans"""),
        ("""<link href="https://fonts.googleapis.com/css2?family=Piazzolla&display=swap" rel="stylesheet">&&Piazzolla""", """Piazzolla"""),
        ("""<link href="https://fonts.googleapis.com/css2?family=Delius&display=swap" rel="stylesheet">&&Delius""", """Delius"""),
        ("""<link href="https://fonts.googleapis.com/css2?family=Itim&display=swap" rel="stylesheet">&&Itim""", """Itim"""),
        ("""<link href="https://fonts.googleapis.com/css2?family=Gloria+Hallelujah&display=swap" rel="stylesheet">&&Gloria Hallelujah""", """Gloria Hallelujah"""),
        ("""<link href="https://fonts.googleapis.com/css2?family=Sansita+Swashed&display=swap" rel="stylesheet">&&Sansita Swashed""", """Sansita Swashed"""),
        ("""<link href="https://fonts.googleapis.com/css2?family=Courier+Prime&display=swap" rel="stylesheet">&&Courier Prime""", """Courier Prime"""),
        ("""<link href="https://fonts.googleapis.com/css2?family=Cousine&display=swap" rel="stylesheet">&&Cousine""", """Cousine"""),
        ("""<link href="https://fonts.googleapis.com/css2?family=PT+Mono&display=swap" rel="stylesheet">&&PT Mono""", """PT Mono"""),
        ("""<link href="https://fonts.googleapis.com/css2?family=Roboto+Mono&display=swap" rel="stylesheet">&&Roboto Mono""", """Roboto Mono"""),
        ("""<link href="https://fonts.googleapis.com/css2?family=Source+Code+Pro&display=swap" rel="stylesheet">&&Source Code Pro""", """Source Code Pro"""),
        ("""<link href="https://fonts.googleapis.com/css2?family=Comic+Neue&display=swap" rel="stylesheet">&&Comic Neue""", """Comic Neue"""),
        ("""<link href="https://fonts.googleapis.com/css2?family=Righteous&display=swap" rel="stylesheet">&&Righteous""", """Righteous"""),
        ("""<link href="https://fonts.googleapis.com/css2?family=Sansita&display=swap" rel="stylesheet">&&Sansita""", """Sansita"""),
    )


class ImageOptions:
    PERCENTAGES = (
            ('width: 10%;', '10%'),
            ('width: 20%;', '20%'),
            ('width: 30%;', '30%'),
            ('width: 40%;', '40%'),
            ('width: 50%;', '50%'),
            ('width: 60%;', '60%'),
            ('width: 70%;', '70%'),
            ('width: 80%;', '80%'),
            ('width: 90%;', '90%'),
            ('width: 100%;', '100%'),
        )

    POSITIONS = (
        ('float: left;', 'float left'),
        ('float: right;', 'float right'),
        ('display: inline;', 'inline'),
        ('display: block;', 'block'),
        ('display: inline-block;', 'inline-block'),
    )

class TextOptions:
    TEXT_COLORS = (
        ('text-light', 'Light'),
        ('text-dark', 'Dark'),
    )

    HEADER_SIZES = (
        ('h1', 'Large'),
        ('h2', 'Medium'),
        ('h3', 'Small')
    )


class SiteLookForm(forms.ModelForm):
    show_home = forms.BooleanField(
        label='Shome Home in Nav',
        required=False,
    )

    show_about = forms.BooleanField(
        label='Show About Page',
        required=False,
    )

    show_sermons = forms.BooleanField(
        label='Show Sermons Page',
        required=False,
    )

    show_music = forms.BooleanField(
        label='Show Worship Music Page',
        required=False,
    )

    show_videos = forms.BooleanField(
        label = 'Show Worship Videos Page',
        required=False,
    )

    show_services = forms.BooleanField(
        label='Show Services Page',
        required=False,
    )

    show_contact = forms.BooleanField(
        label='Show Contact Page',
        required=False,
    )

    show_email_form = forms.BooleanField(
        label="Show Footer 'Learn More' Form",
        required=False,
    )

    footer_tagline = forms.CharField(
        label='Short tagline (26 char. max)',
        required=True,
    )

    footer_about = forms.CharField(
        label='About Statement',
        required=True,
        widget=forms.Textarea(attrs={
            'rows': '3',
            'cols': '40',
            'placeholder': 'Enter a short about statement'
        })
    )

    footer_location = forms.CharField(
        label='Enter Church Address',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'E.g. 123 Mulberry Ln City, ST 12345'
        })
    )

    lat = forms.CharField(
        label='Map Address latitude',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'E.g. 35.956332'
        })
    )

    lon = forms.CharField(
        label='Map Address longitude',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'E.g. -83.923854'
        })
    )

    footer_contact_phone = forms.CharField(
        label='Contact Phone Number',
        required=False,
    )

    footer_contact_email = forms.EmailField(
        label='Contact Email Address',
        required=False,
        widget=forms.EmailInput(attrs={
            'placeholder': 'ContactEmail@example.com'
        })
    )

    footer_text_color = forms.CharField(
        label='Footer text color',
        required=True,
        widget=forms.Select(
            choices=TextOptions.TEXT_COLORS
        )
    )

    navigation_img = forms.FileField(
        label='Nav Image (100x100px - 250x100px recommended):',
        required=False,
        widget=forms.FileInput(attrs={
            'multiple': False,
            'accept': 'image/*'
        })
    )

    favicon = forms.FileField(
        label='Favicon Image',
        required=False,
        widget=forms.FileInput(attrs={
            'multiple': False,
            'accept': 'image/x-icon'
        })
    )

    font = forms.CharField(
        label='Font',
        required=False,
        widget=forms.Select(
            choices=FontOptions.GOOGLE_FONTS
        )
    )

    font_preview = forms.CharField(
        label='Font Preview',
        required=False,
    )

    footer_color = ColorField()

    gallery_color = ColorField()

    class Meta:
        model = SiteLook
        fields = [
            'show_home', 'show_about', 'show_sermons', 'show_music',
            'show_videos', 'show_services', 'show_contact','show_email_form',
            'footer_tagline', 'footer_about', 'footer_location', 'lat', 'lon',
            'footer_contact_phone', 'footer_contact_email', 'footer_text_color',
            'show_email_form', 'font', 'font_preview', 'footer_color', 'gallery_color'
        ]


class HomeForm(forms.ModelForm):
    background_img = forms.FileField(
        label='Splash Image (2000x900px recommended):',
        required=False,
        widget=forms.FileInput(attrs={
            'multiple': False,
            'accept': 'image/*'
        })
    )
    
    alert_banner = forms.CharField(
        label='Alert Banner',
        required=False,
        widget=forms.Textarea(attrs={
            'rows': '4',
            'cols': '40',
            'placeholder': 'Enter an alert to display atop the page; style with HTML.'
        })
    )

    tagline = forms.CharField(
        label='Tagline',
        required=False,
        widget=forms.Textarea(attrs={
            'rows': '2',
            'cols': '40',
            'placeholder': 'Enter a short tagline here.'
        })
    )

    tagline_size = forms.CharField(
        label='Tagline size',
        required=True,
        widget=forms.Select(
            choices=TextOptions.HEADER_SIZES
        )
    )

    tagline_color = ColorField()

    # In the view, make this a link by prepending the
    # mailto in front.
    email_addr = forms.EmailField(
        label='Contact Email',
        required=False,
        widget=forms.EmailInput(attrs={
            'placeholder': 'ContactEmail@example.com'
        })
    )

    facebook_link = forms.URLField(
        label='Facebook Profile',
        required=False,
        widget=forms.URLInput(attrs={
            'placeholder': 'https://www.facebook.com/yourUsername'
        })
    )

    twitter_link = forms.URLField(
        label='Twitter Profile',
        required=False,
        widget=forms.URLInput(attrs={
            'placeholder': 'https://www.twitter.com/yourUsername'
        })
    )

    instagram_link = forms.URLField(
        label='Instagram Profile',
        required=False,
        widget=forms.URLInput(attrs={
            'placeholder': 'https://www.instagram.com/yourUsername'
        })
    )

    youtube_link = forms.URLField(
        label='YouTube Profile',
        required=False,
        widget=forms.URLInput(attrs={
            'placeholder': 'https://www.youtube.com/user/yourChannelName'
        })
    )

    about_label = forms.CharField(
        label='About Link Label',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'E.g. Find out more'
        })
    )

    live_link = forms.URLField(
        label='Live Stream URL',
        required=False
    )

    static_gallery = forms.BooleanField(
        label='Static gallery (no scrolling):',
        required=False,
    )

    gallery_imgs = forms.FileField(
        label='Gallery Images:',
        required=False,
        widget=forms.FileInput(attrs={
            'multiple': True,
            'accept': 'image/*'
        })
    )

    delete_gallery = forms.BooleanField(
        label='Remove all current gallery images?:',
        required=False,
    )

    class Meta:
        model = Home
        fields = [
            'background_img', 'alert_banner', 'tagline', 'tagline_size', 
            'tagline_color', 'email_addr', 'facebook_link', 'twitter_link',
            'instagram_link','youtube_link', 'about_label', 'live_link',
            'gallery_imgs', 'static_gallery', 'delete_gallery'
        ]


class AboutForm(forms.ModelForm):
    show_header_image = forms.BooleanField(
        label='Show Header Image',
        required=False,
    )

    header_image = forms.FileField(
        label='Header Image (~3200x1500px recommended)',
        required=False,
        widget=forms.FileInput(attrs={
            'multiple': False,
            'accept': 'image/*'
        })
    )

    box1_header_text = forms.CharField(
        label='Box 1 Header Text',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'E.g. Our Story'
        })
    )

    box1_img = forms.FileField(
        label='Box 1 Image:',
        required=False,
        widget=forms.FileInput(attrs={
            'multiple': False,
            'accept': 'image/*'
        })
    )

    box1_img_alt = forms.CharField(
        label='Box 1 Image Alt',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Describe the image'
        })
    )

    box1_img_size = forms.CharField(
        label='Box 1 Image Size:',
        required=False,
        widget=forms.Select(
            choices=ImageOptions.PERCENTAGES
        )
    )

    box1_img_position = forms.CharField(
        label='Box 1 Image Position',
        required=False,
        widget = forms.Select(
            choices=ImageOptions.POSITIONS
        )
    )

    box1_content_text = forms.CharField(
        label='Box 1 Content Text - Style with HTML',
        required=False,
        widget=forms.Textarea(attrs={
            'rows': '10',
            'cols': '40',
            'placeholder': ('Enter Box 1\'s content here. You may use HTML tags for styling & linking.')
        })
    )

    delete_box1_img = forms.BooleanField(
        label='Remove current Box 1 Image?:',
        required=False,
    )

    box2_header_text = forms.CharField(
        label='Box 2 Header Text',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'E.g. About Our Pastor'
        })
    )

    box2_img = forms.FileField(
        label='Box 2 Image:',
        required=False,
        widget=forms.FileInput(attrs={
            'multiple': False,
            'accept': 'image/*'
        })
    )

    box2_img_alt = forms.CharField(
        label='Box 2 Image Alt',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Describe the image'
        })
    )

    box2_img_size = forms.CharField(
        label='Box 2 Image Size:',
        required=False,
        widget=forms.Select(
            choices=ImageOptions.PERCENTAGES
        )
    )

    box2_img_position = forms.CharField(
        label='Box 2 Image Position',
        required=False,
        widget = forms.Select(
            choices=ImageOptions.POSITIONS
        )
    )

    delete_box2_img = forms.BooleanField(
        label='Remove current Box 2 Image?:',
        required=False,
    )

    box2_content_text = forms.CharField(
        label='Box 2 Content Text - Style with HTML',
        required=False,
        widget=forms.Textarea(attrs={
            'rows': '10',
            'cols': '40',
            'placeholder': ('Enter Box 2\'s content here. You may use HTML tags for styling & linking.')
        })
    )

    gallery_imgs = forms.FileField(
        label='Gallery Images:',
        required=False,
        widget=forms.FileInput(attrs={
            'multiple': True,
            'accept': 'image/*'
        })
    )

    static_gallery = forms.BooleanField(
        label='Static gallery (no scrolling):',
        required=False,
    )

    delete_gallery = forms.BooleanField(
        label='Remove all current gallery images?:',
        required=False,
    )

    class Meta:
        model = About
        fields = [ 
            'show_header_image', 'header_image',
            'box1_header_text', 'box1_content_text', 'box1_img', 'box1_img_alt',
            'box1_img_size', 'box1_img_position','box2_header_text', 'box2_content_text',
            'box2_img', 'box2_img_alt', 'box2_img_size', 'box2_img_position', 'gallery_imgs',
            'static_gallery', 'delete_gallery', 'delete_box1_img', 'delete_box2_img'
        ]


class ServicesForm(forms.ModelForm):
    show_header_image = forms.BooleanField(
        label='Show Header Image',
        required=False,
    )

    header_image = forms.FileField(
        label='Header Image (~3200x1500px recommended)',
        required=False,
        widget=forms.FileInput(attrs={
            'multiple': False,
            'accept': 'image/*'
        })
    )

    box1_header_text = forms.CharField(
        label='Box 1 Header Text',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'E.g. Weekly Services'
        })
    )

    box1_content_text = forms.CharField(
        label='Box 1 Content Text - Style with HTML',
        required=False,
        widget=forms.Textarea(attrs={
            'rows': '10',
            'cols': '40',
            'placeholder': ('Enter Box 1\'s content here. You may use HTML tags for styling & linking.')
        })
    )

    box1_img = forms.FileField(
        label='Box 1 Image:',
        required=False,
        widget=forms.FileInput(attrs={
            'multiple': False,
            'accept': 'image/*'
        })
    )

    box1_img_alt = forms.CharField(
        label='Box 1 Image Alt',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Describe the image'
        })
    )

    box1_img_size = forms.CharField(
        label='Box 1 Image Size:',
        required=False,
        widget=forms.Select(
            choices=ImageOptions.PERCENTAGES
        )
    )

    box1_img_position = forms.CharField(
        label='Box 1 Image Position',
        required=False,
        widget = forms.Select(
            choices=ImageOptions.POSITIONS
        )
    )

    delete_box1_img = forms.BooleanField(
        label='Remove current Box 1 Image?:',
        required=False,
    )

    box1_link = forms.CharField(
        label='Box 1 Link',
        required=False
    )

    box1_link_desc = forms.CharField(
        label='Box 1 Link Text',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Label the link'
        })
    )

    box2_header_text = forms.CharField(
        label='Box 2 Header Text',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'E.g. Bible Study'
        })
    )

    box2_content_text = forms.CharField(
        label='Box 2 Content Text - Style with HTML',
        required=False,
        widget=forms.Textarea(attrs={
            'rows': '10',
            'cols': '40',
            'placeholder': ('Enter Box 2\'s content here. You may use HTML tags for styling & linking.')
        })
    )

    box2_img = forms.FileField(
        label='Box 2 Image:',
        required=False,
        widget=forms.FileInput(attrs={
            'multiple': False,
            'accept': 'image/*'
        })
    )

    box2_img_alt = forms.CharField(
        label='Box 2 Image Alt',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Describe the image'
        })
    )

    box2_img_size = forms.CharField(
        label='Box 2 Image Size:',
        required=False,
        widget=forms.Select(
            choices=ImageOptions.PERCENTAGES
        )
    )

    box2_img_position = forms.CharField(
        label='Box 2 Image Position',
        required=False,
        widget = forms.Select(
            choices=ImageOptions.POSITIONS
        )
    )

    delete_box2_img = forms.BooleanField(
        label='Remove current Box 2 Image?:',
        required=False,
    )

    box2_link = forms.CharField(
        label='Box 2 Link',
        required=False
    )

    box2_link_desc = forms.CharField(
        label='Box 2 Link Text',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Label the link'
        })
    )

    box3_header_text = forms.CharField(
        label='Box 3 Header Text',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'E.g. Prayer Ministry'
        })
    )

    box3_content_text = forms.CharField(
        label='Box 3 Content Text - Style with HTML',
        required=False,
        widget=forms.Textarea(attrs={
            'rows': '10',
            'cols': '40',
            'placeholder': ('Enter Box 3\'s content here. You may use HTML tags for styling & linking.')
        })
    )

    box3_img = forms.FileField(
        label='Box 3 Image:',
        required=False,
        widget=forms.FileInput(attrs={
            'multiple': False,
            'accept': 'image/*'
        })
    )

    box3_img_alt = forms.CharField(
        label='Box 3 Image Alt',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Describe the image'
        })
    )

    box3_img_size = forms.CharField(
        label='Box 3 Image Size:',
        required=False,
        widget=forms.Select(
            choices=ImageOptions.PERCENTAGES
        )
    )

    box3_img_position = forms.CharField(
        label='Box 3 Image Position',
        required=False,
        widget = forms.Select(
            choices=ImageOptions.POSITIONS
        )
    )

    delete_box3_img = forms.BooleanField(
        label='Remove current Box 3 Image?:',
        required=False,
    )

    box3_link = forms.CharField(
        label='Box 3 Link',
        required=False
    )

    box3_link_desc = forms.CharField(
        label='Box 3 Link Text',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Label the link'
        })
    )

    show_prayer_form = forms.BooleanField(
        label='Show Prayer Form',
        required=False,
    )

    class Meta:
        model = Services
        fields = [
            'show_header_image', 'header_image',
            'box1_header_text', 'box1_content_text', 'box1_img', 'box1_img_alt',
            'box1_img_size', 'box1_img_position', 'delete_box1_img', 'box1_link',
            'box1_link_desc', 'box2_header_text', 'box2_content_text', 'box2_img',
            'box2_img_alt', 'box2_img_size', 'box2_img_position', 'delete_box2_img',
            'box2_link', 'box2_link_desc', 'box3_header_text', 'box3_content_text',
            'box3_img', 'box3_img_alt', 'box3_img_size', 'box3_img_position',
            'delete_box3_img', 'box3_link', 'box3_link_desc','show_prayer_form'
        ]


class ContactForm(forms.ModelForm):
    show_header_image = forms.BooleanField(
        label='Show Header Image',
        required=False,
    )

    header_image = forms.FileField(
        label='Header Image (~3200x1500px recommended)',
        required=False,
        widget=forms.FileInput(attrs={
            'multiple': False,
            'accept': 'image/*'
        })
    )

    phone_fax_header_text = forms.CharField(
        label='Phone & Fax Header',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'E.g. Phone and Fax'
        })
    )

    contact_phone = forms.CharField(
        label='Contact Phone Number',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Tip: Don\'t include spaces'
        })
    )

    contact_fax = forms.CharField(
        label='Contact Fax Number',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Tip: Don\'t include spaces'
        })
    )


    addr_mail_header_text = forms.CharField(
        label='Address & Mail Header',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'E.g. Address and Mail'
        })
    )

    contact_address = forms.CharField(
        label='Church Address',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'E.g. 123 Mulberry Ln City, ST 12345'
        })
    )

    contact_mailbox = forms.CharField(
        label='Mail/P.O. Box',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'E.g. P.O. Box 8'
        })
    )

    contact_email_addr = forms.EmailField(
        label='Contact Email Address',
        required=False,
        widget=forms.EmailInput(attrs={
            'placeholder': 'ContactEmail@example.com'
        })
    )

    show_contact_form = forms.BooleanField(
        label='Show Contact Form',
        required=False,
    )

    class Meta:
        model = Contact
        fields = [
            'show_header_image', 'header_image',
            'phone_fax_header_text', 'contact_phone', 'contact_fax',
            'addr_mail_header_text', 'contact_address', 'contact_mailbox',
            'contact_email_addr', 'show_contact_form'
        ]


class SermonsHeaderForm(forms.ModelForm):
    show_header_image = forms.BooleanField(
        label='Show Header Image',
        required=False,
    )

    header_image = forms.FileField(
        label='Header Image (~3200x1500px recommended)',
        required=False,
        widget=forms.FileInput(attrs={
            'multiple': False,
            'accept': 'image/*'
        })
    )

    header_text = forms.CharField(
        label='Header Text',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'E.g. Explore our library of downloadable sermons'
        })
    )

    class Meta:
        model = SermonsHeader
        fields = [ 'show_header_image', 'header_image', 'header_text' ]


class MusicHeaderForm(forms.ModelForm):
    show_header_image = forms.BooleanField(
        label='Show Header Image',
        required=False,
    )

    header_image = forms.FileField(
        label='Header Image (~3200x1500px recommended)',
        required=False,
        widget=forms.FileInput(attrs={
            'multiple': False,
            'accept': 'image/*'
        })
    )

    header_text = forms.CharField(
        label='Header Text',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'E.g. Explore our library of downloadable music'
        })
    )

    class Meta:
        model = MusicHeader
        fields = [ 'show_header_image', 'header_image', 'header_text' ]


class VideosHeaderForm(forms.ModelForm):
    show_header_image = forms.BooleanField(
        label='Show Header Image',
        required=False,
    )

    header_image = forms.FileField(
        label='Header Image (~3200x1500px recommended)',
        required=False,
        widget=forms.FileInput(attrs={
            'multiple': False,
            'accept': 'image/*'
        })
    )

    header_text = forms.CharField(
        label='Header Text',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'E.g. Explore our library of downloadable music'
        })
    )

    class Meta:
        model = VideosHeader
        fields = [ 'show_header_image', 'header_image', 'header_text' ]


class SpeakerForm(forms.ModelForm):

    class Meta:
        model = Speaker
        fields = [ 'name' ]


class ArtistForm(forms.ModelForm):

    class Meta:
        model = Artist
        fields = [ 'name' ]


class SermonForm(forms.ModelForm):
    audio_file = forms.FileField(
        label='Audio File',
        required=False, # Not-required for purpose of editing; they can always delete.
        widget=forms.FileInput(attrs={
            'multiple': False,
            'accept': 'audio/*'
        })
    )

    title = forms.CharField(
        label='Title',
        required=True,
    )

    date = forms.DateField(
        label = 'Sermon Date',
        required=True,
        widget=forms.DateInput(attrs={
            'placeholder': 'E.g. 09/20/20'
        })
    )

    # Omitting audio_file from fields keeps it from also being stored in
    # root project dir.

    class Meta:
        model = Sermon
        fields = [ 'title', 'date' ]


class MusicForm(forms.ModelForm):
    audio_file = forms.FileField(
        label='Audio File',
        required=False, # Not-required for purpose of editing; they can always delete.
        widget=forms.FileInput(attrs={
            'multiple': False,
            'accept': 'audio/*'
        })
    )

    title = forms.CharField(
        label='Title',
        required=True,
    )

    date = forms.DateField(
        label='Song Date',
        required=True,
        widget=forms.DateInput(attrs={
            'placeholder': 'E.g. 09/20/20'
        })
    )

    # Omitting audio_file from fields keeps it from also being stored in
    # root project dir.

    class Meta:
        model = Song
        fields = [ 'title', 'date' ]


class WorshipVideoForm(forms.ModelForm):
    iframe = forms.CharField(
        label='Iframe Embed Link',
        required=True
    )

    title = forms.CharField(
        label='Title',
        required=True
    )

    date = forms.DateField(
        label = 'Video Date',
        required = True,
        widget=forms.DateInput(attrs={
            'placeholder': 'E.g. 09/20/20'
        })
    )

    description = forms.CharField(
        label='Description',
        required=False,
        widget=forms.Textarea(attrs={
            'rows': '4',
            'cols': '40',
            'placeholder': 'Describe this worship service.'
        })
    )

    bulletin_file = forms.FileField(
        label = 'Bulletin PDF',
        required = False,
        widget = forms.FileInput(attrs={
            'multiple': False,
            'accept': 'application/pdf'
        })
    )

    class Meta:
        model = WorshipVideo
        fields = [ 'iframe', 'title', 'date', 'description', 'bulletin_file' ]


class SEOForm(forms.ModelForm):
    meta_title = forms.CharField(
        label='Site Title',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'E.g. Lakeshore Road Baptist Church'
        })
    )

    meta_description = forms.CharField(
        label='Site Description',
        required=True,
        widget=forms.Textarea(attrs={
            'rows': '2',
            'cols': '40',
            'placeholder': 'This is our pitch. Sell our organization/site to readers.'
        })
    )

    meta_keywords = forms.CharField(
        label='Site Keywords',
        required=True,
        widget=forms.Textarea(attrs={
            'rows': '4',
            'cols': '40',
            'placeholder': ('Help search engines identify the site.\n'
                            'Ex. keywords: christian, church, baptist,'),
        })
    )

    meta_author = forms.CharField(
        label='Site Author',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'E.g. Lakeshore Road Baptist Church'
        })
    )

    robots_index = forms.BooleanField(
        label='Let bots index pages',
        required=False,
    )

    robots_follow = forms.BooleanField(
        label='Let bots crawl links',
        required=False,
    )

    robots_txt = forms.FileField(
        label='Upload a robots.txt file',
        required=False,
        widget=forms.FileInput(attrs={
            'multiple': False,
            'accept': 'text/plain'
        })
    )

    class Meta:
        model = SEO
        fields = [
            'meta_title', 'meta_description', 'meta_keywords', 'meta_author',
            'robots_index', 'robots_follow', 'robots_txt'
        ]


class NoLogIPForm(forms.ModelForm):
    ip = forms.GenericIPAddressField(
        label='IP Address',
        required=True,
    )
    comment = forms.CharField(
        label='Comment',
        required=False,
    )
    class Meta:
        model = NoLogIPModel
        fields = [ 'ip', 'comment' ]


class DenylistEmailForm(forms.ModelForm):
    email_addr = forms.EmailField(
        label='Email Address',
        required=True,
    )

    comment = forms.CharField(
        label='Comment',
        required=False,
    )

    class Meta:
        model = DenylistEmailModel
        fields = [ 'email_addr', 'comment' ]


class EmailAccountForm(forms.ModelForm):
    email_addr = forms.EmailField(
        label='Email Recipient',
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'SiteEmail@example.com'
        })
    )

    class Meta:
        model = EmailAccount
        fields = [ 'email_addr', ]