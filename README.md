# lrbc_site
Django web application to manage and host a church website.

![Preview of the web application](./screenshots/preview.png)

## Requirements

- Python 3.8.3
- Some basic Django familiarity.

## About

I originally started developing this project for my local church in early summer
when it was clear that we needed to prepare to move our services online. Managing
our site through Weebly, I wanted repetitive things that I would do such as adding
new sermon audio and music to be simpler since this required me to drag and drop
new components each time. Further, the site needed list filtering/searching because
I knew that eventually the content would be a lot to simply scroll through.

I deployed a cruder version of this project a few months ago using nginx and gunicorn
on a DigitalOcean server and moved our church's domain (lrbclife.org) from the Weebly
site to the DigitalOcean server; this gives me complete control of the server and saves
us between $7 and $8 per month. I have been building up the functionality of the site
over the last few months. My more recent addtions include the REST API which allows us
to visualize page views and unique page visits over days, weeks, and months using
Chart.js and the ability to export these database records for direct insertion into
another database.

This project is fully responsive and I feel that it now has the minimal features
necessary for it to be useful for a small church to manage their website on this
Django app (and some bonus features such as the exportable view and visit data).
Without further ado, let's get into the setup...

## Setup

### 1) Clone the repo.

### 2) Create a virtualenv in the lrbc_site root dir
    cd lrbc_site; python3 -m venv venv

### 3) Install the requirements
    source venv/bin/activate
    pip3 install -r requirements.txt

### 4) Make the migrations
Please include the skip-checks flags; if you do not—well—you have
been warned.

    python3 manage.py makemigrations admin_pages --skip-checks
    python3 manage.py makemigrations site_pages --skip-checks
    python3 manage.py migrate --skip-checks

### 5) Run the initial_setup script
The app is almost set up for you to run, but you will need to run the
initial_setup.py script to create the appropriate static directories,
populate the DB with the neccessary rows, and allow you to create an
initial account to log into. To do this enter the
commands below:

    python3 manage.py shell
    exec(open('initial_setup.py').read())
    exit()

Now that the insertions have been made, I suggest changing the file
extension of the initial_setup.py file so there isn't a chance
that you accidently execute it again and overwrite your data.

### 6) Run the server
You are now ready to test the server by running the following command:

    python3 manage.py runserver 127.0.0.1:8000

Try logging into the site management menu using your newly created
credentials at 127.0.0.1:8000/users/login or 127.0.0.1:8000/admin_pages.


### Managing page content/access

You will notice several options which I will do my best to begin documenting,
however, the ones you will access most frequently are those under "Manage Pages".
These control the content of the navigation and footer and each page. The "Site Look"
form also allows you to select which pages are accessible and which
you may want to keep hidden. I also highly recommend filling out the SEO information
once this app is running in production so your website will get found.

TinyMCE registration:

You will notice that I have used TinyMCE to provide text formatting tools for each
of the textareas in "Manage Pages". It will display a message that it is unregistered
with an API key. You can follow the link provided in the message to create a TinyMCE
account. Then add your domain name to be able to use your key with that domain.
Open "lrbc_site/settings.py" and replace the script stored to the TINYMCE_SCRIPT 
variable on line 20 with the script you were provided TinyMCE Quick-Start step
following your registration.


### Ensuring forms are "live"

You will notice that I have three different forms which you can enable. In the
"Nav & Footer" form, you will see a checkbox for "Show Footer 'Learn More' Form".
Second, in the "Services Page" form, you will see a checkbox for "Show Prayer Form",
and last, you will see a checkbox for "Show Contact Form". You can enable these forms
but two things need to be done before the submitted form data will actually be sent
somewhere:

#### 1) Scroll to the bottom lrbc_site/lrbc_site/settings.py to find the email settings.
Configure the email settings with an email account which supports SMTP. These settings
are neccessary because this is the email account you will use to send your form data.
I have left some example settings for Gmail using TLS. There are many good tutorials
for these settings such as (https://data-flair.training/blogs/django-send-email/).

#### 2) Configure the email account that will receive the form data; it can be the same
address if you want. To do this, navigate to 127.0.0.1:8000/admin_pages -> Accounts
 -> Email. Enter your recipient email address in the resulting form. You will need
 to restart the Django app; you may press (Ctrl-c) to exit it and then re-enter the
 runserver command.


## Notes for deploying

If you would like to use this app for your church, that is why I have made it public
so go for it. There are several things you should note.

#### 1) Change the security key

You will need to change the security key in lrbc_site/lrbc_site/settings.py since it
is publically available; it just needs to be long and suffficiently random. There is
even a website for generating these: (https://djecrety.ir/).

#### 2) Add your hostname

You will need to add your hostname in the ALLOWED_HOSTS list in the settings. You may
also need 0.0.0.0 as a host to initially test on a production server. It is good to
include 'yourdomain.com' as well as 'www.yourdomain.com' as allowed hosts. Of course,
if you have no domain name, you will need to purchase one and read your server host's
and/or your DNS host's documentation on pointing it to your server on which you host
the Django app.

#### 3) Turn off debug

You may want debug on to initially test your site before adding SSL encryption but
don't forget to set DEBUG = False in the settings after initial testing.

#### 4) Put your IP address on the No-Log List

If you are administrating the website, you probably access the pages often. While this
is not going to inflate unique visits too badly (a *unique* visit means the server had
to issue a new cookie; your browser will use the same cookie thereafter until it is
closed), but you can easily inflate the page views since each page view is logged in
the database (you can delete views and visits from the admin menu -> "Views and SEO" ->
"Pages Viewed" or "Unique Visits"; the hamburger menu on the top right of either
of those pages will have options to clear these records.

To prevent inflating the views, you can put your IPv4 address in the IP No-Log List.
From the admin menu choose "Denylists" -> "IP No-Log List". Anyone who is editing 
the site frequently probably ought to put her or his IP address on the list so
the page view metrics are not inflated.

> By the way, the cookies I use store absolutely no sensitive information,
> the only thing they store is a timestamp of the browser's last request.
> I log the location information from unique visits simply by using a lib
> called ip2geotools (https://pypi.org/project/ip2geotools/) to lookup
> the country, region, and city of the IP address that appears in the
> request header. The IP address itself is not stored.

### Recommendations

I will try to write some good documentation -- not only on this app's features but for
deploying the app on an Ubuntu web server which I did just a few months ago. Although some
reading this will have much more expertise with server deployments than myself, I generally
find it easiest to use an Ubuntu server; I prefer good ole 18.04. Additionally, I recommend
using nginx as your web server. nginx will need a socket to communicate with the Django app
which is where the Python package, gunicorn comes into play. The documentation that greatly
helped me set up this app on our Church's web server is:
(https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-18-04)
Of course, I stuck with a simple SQLite3 database instead of PostgreSQL but the rest of the
instructions were applicable, I believe.

You will of course need for your traffic to be encrypted. I wouldn't even log into the site until
this is done! The easiest way in the world to configure HTTPS is using Certbot and fortunately
there is good documentation (also from DigitalOcean) on doing just that:
(https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-18-04)


