from admin_pages.models import EmailAccount
from django.core.mail import send_mail

recip_email_acct = EmailAccount.objects.get(id=1)
sender = 'churchinsite.noreply@gmail.com'
recipient = ''

def refresh_email_recipient():
    """This function is designed so that when the EmailAccount
    object with id 1 is updated in admin_pages.views, the module
    calls this function which simply re-copies the email_addr
    string of the object to the global recipient string. This
    way, the recipient will always be current.
    """
    global recip_email_acct, recipient
    recip_email_acct.refresh_from_db()
    recipient = recip_email_acct.email_addr


def send_contact_email(time, contact_email):
    """Sends an email to the recipient timestamped with the value of
    the param, time and a message pertaining to and including the
    form data -- which in this case is simply an email address of
    someone who would like information about the church.

    Parameters:
    time (str): A timestamp in the format '%m/%d/%y %I:%M %p' (see datetime documentation).
    contact_email (str): A contact email address from a submitted form's data.
    """
    body = time + ": " + contact_email + " would like to find out more about your church."
    try:
        send_mail(
            'New Email Contact Request',
            body,
            sender,
            [recipient],
            fail_silently=False,
        )
    except:
        pass


def send_prayer_request(time, name, comment):
    """Sends an email to the recipient timestamped with the value of
    the param, time and a message pertaining to and including the
    form data -- which in this case is a name and a comment from
    someone who has submitted a prayer request.

    Parameters:
    time (str): A timestamp in the format '%m/%d/%y %I:%M %p' (see datetime documentation).
    name (str): A name from a submitted form's data.
    comment (str): A comment from a submitted form's data.
    """
    body = time + " - Prayer Request for " + name + ":\n\n" + comment
    try:
        send_mail(
            'New Prayer Request',
            body,
            sender,
            [recipient],
            fail_silently=False,
        )
    except:
        pass


def send_contact_form(time, name, email, comment):
    """Sends an email to the recipient timestamped with the value of
    the param, time and a message pertaining to and including the
    form data -- which in this case is a name and a comment from
    someone who has submitted a prayer request.

    Parameters:
    time (str): A timestamp in the format '%m/%d/%y %I:%M %p' (see datetime documentation).
    name (str): A name from a submitted form's data.
    comment (str): A comment from a submitted form's data.
    """
    body = time + " - " + name + " (" + email + "):\n\n" + comment
    try:
        send_mail(
            'New Contact Request',
            body,
            sender,
            [recipient],
            fail_silently=False,
        )
    except:
        pass