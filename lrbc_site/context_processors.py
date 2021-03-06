from admin_pages.models import SiteLook, SEO
from site_pages.forms import *
from lrbc_site import settings

def add_to_context(request):
    site_look = SiteLook.objects.get(id=1)
    seo = SEO.objects.get(id=1)

    try:
        f = site_look.font.split('&&')
    except:
        f[0] = '<link href="https://fonts.googleapis.com/css2?family=Mulish&display=swap" rel="stylesheet">'
        f[1] = "Mulish"

    return {
        'email_contact_form': EmailContactForm(),
        'prayer_request_form': PrayerRequestForm(),
        'viewer_contact_form': ViewerContactForm(),
        'meta_title': seo.meta_title,
        'meta_description': seo.meta_description,
        'meta_author': seo.meta_author,
        'meta_keywords': seo.meta_keywords,
        'robots_index': seo.robots_index,
        'robots_follow': seo.robots_follow,
        'show_home': site_look.show_home,
        'show_about': site_look.show_about,
        'show_leadership': site_look.show_leadership,
        'show_sermons': site_look.show_sermons,
        'show_music': site_look.show_music,
        'show_videos': site_look.show_videos,
        'show_services': site_look.show_services,
        'show_contact': site_look.show_contact,
        'footer_tagline': site_look.footer_tagline,
        'footer_about': site_look.footer_about,
        'footer_location': site_look.footer_location,
        'navigation_img_size': site_look.navigation_img_size,
        'footer_lat': site_look.lat,
        'footer_lon': site_look.lon,
        'footer_color': site_look.footer_color,
        'gallery_color': site_look.gallery_color,
        'footer_contact_email': site_look.footer_contact_email,
        'footer_contact_phone': site_look.footer_contact_phone,
        'font': f[0],
        'font_family': f[1],
        'footer_text_color': site_look.footer_text_color,
        'show_email_form': site_look.show_email_form,
        'tinymce_script': settings.TINYMCE_SCRIPT
    }