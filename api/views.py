from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect

from rest_framework.views import APIView
from rest_framework.response import Response

from site_pages.models import Page, Visitor
from admin_pages.models import SiteLook
from . import db_exporter
from .forms import *

from datetime import datetime as dt, timedelta
import threading


pages_allowed = [ 'Index' ]

# Used to get day string by using datetime.datetime object's
# weekday value as the key.
DAYS = {
    0: 'Monday',
    1: 'Tuesday',
    2: 'Wednesday',
    3: 'Thursday',
    4: 'Friday',
    5: 'Saturday',
    6: 'Sunday',
}


def update_pages_allowed():
    """Updates the list, pages_allowed by checking the
    SiteLook object with id 1 to see if the flag allowing
    the page is true or not. This function is called after
    a change is made in admin_pages.views' manage_site_look
    function.
    """
    global pages_allowed
    site_look = SiteLook.objects.get(id=1)
    pages_allowed = pages_allowed[:1] # Index is always visible.
    if (site_look.show_about):
        pages_allowed.append('About')
    if (site_look.show_leadership):
        pages_allowed.append('Leadership')
    if (site_look.show_sermons):
        pages_allowed.append('Sermons')
    if (site_look.show_music):
        pages_allowed.append('Worship Music')
    if (site_look.show_videos):
        pages_allowed.append('Worship Videos')
    if (site_look.show_services):
        pages_allowed.append('Services')
    if (site_look.show_contact):
        pages_allowed.append('Contact')


def get_dates(enddate, num_days):
    """Creates a list of weekdays starting with the date string,
    enddate and working backwards to append each previous weekday
    (num_days - 1) times. Each string in the list is formatted
    like: "Monday, 8/3", "Sunday, 8/4", etc. The function also
    creates a separate multidimensional list containing each date's,
    day, month, and year numeric value (if the first date were Aug 3,
    2020, then numeric_dates[0] would look like this:
    ['03', '08', '2020']).

    Parameters:
    enddate (str): The date string that serves as a starting point for the calculations; in the format '%Y-%m-%d' (see datetime documentation).
    num_days (int): The number of weekdays and numeric day values that should be stored in the list.

    Returns:
    List:A list of strings containing weekday labels each in the form, "Monday, 8/3", etc.
    List:A multidimensional list of strings containing the numeric values of each dates, day, month, and year.
    str:The current year
    """
    week_days = []
    numeric_dates = []

    for i in range(0, num_days):
        numeric_dates.append([])

    # Getting 1st day:
    now = dt.strptime(enddate, '%Y-%m-%d').replace(microsecond=0)
    day_lbl = ( DAYS[now.weekday()] + ', ' + str(now.month) +
                '/' + str(now.day) )
    week_days.append(day_lbl)
    curr_date = now.__str__().split(' ')[0]
    curr_date_split = curr_date.split('-')
    numeric_dates[0].append(curr_date_split[2])
    numeric_dates[0].append(curr_date_split[1])
    numeric_dates[0].append(curr_date_split[0])

    # Getting previous (num_days - 1) days:
    for i in range(1, num_days): # Getting the previous six days from today
        day = now - timedelta(days=1)
        day = day.replace(microsecond=0)
        now = day # Make now the previous day for next iteration.
        day_lbl = ( DAYS[day.weekday()] + ', ' + str(day.month) +
                    '/' + str(day.day) )
        week_days.append(day_lbl)
        day_split = day.__str__().split(' ')[0].split('-') # Extract date string and split month, day, year
        numeric_dates[i].append(day_split[2]) # Day
        numeric_dates[i].append(day_split[1]) # Month
        numeric_dates[i].append(day_split[0]) # Year
    
    return week_days, numeric_dates


def delete_records(time_period, enddate, model):
    """Deletes database records of the type indicated by the model
    param beginning with the enddate over the specified time period.
    If the time period value accepted by the time_period param == 0,
    this means to delete all records of type model. Otherwise, the
    time period is a literal number of days to delete starting with
    the date specified by string enddate and working backwards to
    delete records of the previous (time_period - 1) days as well.

    Parameters:
    enddate (str): The date string that serves as a starting point for the calculations; in the format '%Y-%m-%d' (see datetime documentation).
    time_period (int): The number of days including enddate and the previous (time_period - 1) days from enddate for which records will be deleted.
    model (str): The name of the model to delete entries from.

    Returns:
    delete_ok (bool): A status flag to indicate whether all deletions were successful or not.
    """
    delete_ok = True
    try:
        if time_period == 0:
            if (model == 'Page'):
                Page.objects.all().delete()
            else:
                Visitor.objects.all().delete()
        else:
            now = dt.strptime(enddate, '%Y-%m-%d')
            now_str = now.__str__().split(' ')[0].split('-')
            if (model == 'Page'):
                for i in range(0, time_period):
                    Page.objects.filter(year=now_str[0], 
                        month=now_str[1], day=now_str[2]).delete()
                    now = now - timedelta(days=1)
                    now_str = now.__str__().split(' ')[0].split('-')
            else:
                for i in range(0, time_period):
                    Visitor.objects.filter(year=now_str[0],
                                month=now_str[1], day=now_str[2]).delete()
                    now = now - timedelta(days=1)
                    print(now)
                    now_str = now.__str__().split(' ')[0].split('-')
    except:
        delete_ok = False
    
    return delete_ok # Calling function will use this to either return HTTP 200 or 500.


class DailyPageViews(APIView):
    """Aggregates page views per day and per page from the Page model
    per a 7-day period spanning from the date in string enddate to the
    previous 6 days from enddate.

    Parameters:
    self (DailyPageViews): The DailyPageViews object (a child of rest_framework.views.APIView).
    request (HTTPRequest): The request object.
    enddate (str): The date string that serves as a starting point for the calculations; in the format '%Y-%m-%d' (see datetime documentation).
    format (str): A format suffix pattern; by saying None, I am accepting a valid HTTP request regardless of whether it is a JSON request or not.

    Returns:
    Response (rest_framework.response.Response): A response object whose Content-Type should always be JSON text.
    """
    def get(self, request, enddate, format=None):
        week_days, numeric_dates = get_dates(enddate, 7)

        counts_per_day = []
        for i in range(0, 7):
            daily_counts = []
            pages_by_day = Page.objects.filter(day=numeric_dates[i][0], month=numeric_dates[i][1],
                                                year=numeric_dates[i][2])
            for j in range(0, len(pages_allowed)):
                pages_by_name = pages_by_day.filter(page_name=pages_allowed[j])
                daily_counts.append(len(pages_by_name))
            counts_per_day.append(daily_counts)

        data = {
            "weekday_labels": week_days,
            "page_labels": pages_allowed,
            "counts_per_day": counts_per_day
        }
        return Response(data)


class WeeklyPageViews(APIView):
    """Aggregates page views per week and per page from the Page model
    per a 7-day period spanning from the date in string enddate to the
    previous 6 days from enddate.

    Parameters:
    self (WeeklyPageViews): The WeeklyPageViews object (a child of rest_framework.views.APIView).
    request (HTTPRequest): The request object.
    enddate (str): The date string that serves as a starting point for the calculations; in the format '%Y-%m-%d' (see datetime documentation).
    format (str): A format suffix pattern; by saying None, I am accepting a valid HTTP request regardless of whether it is a JSON request or not.

    Returns:
    Response (rest_framework.response.Response): A response object whose Content-Type should always be JSON text.
    """
    def get(self, request, enddate, format=None):
        week_days, numeric_dates = get_dates(enddate, 7)

        weekly_counts = [0] * len(pages_allowed)
        for i in range(0, 7):
            pages_by_day = Page.objects.filter(day=numeric_dates[i][0], month=numeric_dates[i][1],
                                                year=numeric_dates[i][2])
            for j in range(0, len(pages_allowed)):
                pages_by_name = pages_by_day.filter(page_name=pages_allowed[j])
                temp = weekly_counts[j]
                weekly_counts[j] = (temp + len(pages_by_name))

        data = {
            "week_label": week_days[6] + " ⁠— " + week_days[0],
            "page_labels": pages_allowed,
            "weekly_counts": weekly_counts
        }
        return Response(data)


class MonthlyPageViews(APIView):
    """Aggregates page views per 30 days and per page from the Page model
    per a 30-day period spanning from the date in string enddate to the
    previous 29 days from enddate. Additionally this aggregates the total
    number of page views over the 30-day period and it finds the average
    time a page was viewed over the period.

    Parameters:
    self (MonthlyPageViews): The MonthlyPageViews object (a child of rest_framework.views.APIView).
    request (HTTPRequest): The request object.
    enddate (str): The date string that serves as a starting point for the calculations; in the format '%Y-%m-%d' (see datetime documentation).
    format (str): A format suffix pattern; by saying None, I am accepting a valid HTTP request regardless of whether it is a JSON request or not.

    Returns:
    Response (rest_framework.response.Response): A response object whose Content-Type should always be JSON text.
    """
    def get(self, request, enddate, format=None):
        week_days, numeric_dates = get_dates(enddate, 30)

        monthly_counts = [0] * len(pages_allowed)
        hours = 0
        num_views = 0
		
        for i in range(0, 30):
            pages_by_day = Page.objects.filter(day=numeric_dates[i][0], month=numeric_dates[i][1],
                                                year=numeric_dates[i][2])
            for p in pages_by_day:
                hours += (int(p.time[:2])) # Slice hour from time and parse as int -> add to total
                num_views += 1
            for j in range(0, len(pages_allowed)):
                pages_by_name = pages_by_day.filter(page_name=pages_allowed[j])
                temp = monthly_counts[j]
                monthly_counts[j] = (temp + len(pages_by_name))

        # This will give modulo by zero error if no hours (no views):
        try:
            hr = ( hours // num_views )
            if (hr == 12): # Make hour 12-hr format
                hr_str = str(hr) + ' PM'
            elif (hr > 12):
                hr = (hr - 12)
                hr_str = str(hr) + ' PM'
            else:
                hr_str = str(hr) + ' AM'
        except:
            hr_str = 'None'

        data = {
            "month_label": week_days[27] + " ⁠— " + week_days[0],
            "page_labels": pages_allowed,
            "monthly_counts": monthly_counts,
            "avg_view_hour": hr_str,
            "total_views": num_views
        }
        return Response(data)


class DailyVisitors(APIView):
    """Aggregates page visits per day from the Visitor model
    per a 7-day period spanning from the date in string enddate to the
    previous 6 days from enddate. Additionally, the function groups
    the visits from the same country and region and city together and
    provides labels for the count of each city.

    Parameters:
    self (DailyVisitors): The DailyVisitors object (a child of rest_framework.views.APIView).
    request (HTTPRequest): The request object.
    enddate (str): The date string that serves as a starting point for the calculations; in the format '%Y-%m-%d' (see datetime documentation).
    format (str): A format suffix pattern; by saying None, I am accepting a valid HTTP request regardless of whether it is a JSON request or not.

    Returns:
    Response (rest_framework.response.Response): A response object whose Content-Type should always be JSON text.
    """
    def get(self, request, enddate, format=None):
        week_days, numeric_dates = get_dates(enddate, 7)

        daily_cities_lists = []
        daily_cities_counts = []

        for i in range(0, 7):
            cities_dict = {}
            cities_list   = []
            cities_values = []
            visitors_by_day = Visitor.objects.filter(
                                    day=numeric_dates[i][0], month=numeric_dates[i][1],
                                    year=numeric_dates[i][2]
                                )
            for visitor in visitors_by_day:
                city = visitor.city + ', ' + visitor.region + ', ' + visitor.country
                try:
                    cities_dict[city] += 1
                except: # Initial dictionary entry for region and city
                    cities_dict[city] = 1

            for key in cities_dict.keys():
                cities_list.append(key)
                cities_values.append(cities_dict[key])

            daily_cities_lists.append(cities_list)
            daily_cities_counts.append(cities_values)

        data = {
            'weekday_labels': week_days,
            'city_labels': daily_cities_lists,
            'counts_per_day': daily_cities_counts
        }

        return Response(data)


class WeeklyVisitors(APIView):
    """Aggregates page visits per week from the Visitor model
    per a 7-day period spanning from the date in string enddate to the
    previous 6 days from enddate. Additionally, the function groups
    the visits from the same country and region and city together and
    provides labels for the count of each city for the top 10 cities.
    Any views from cities that don't make up the top 10 are grouped
    together under the label of 'Other'.

    Parameters:
    self (WeeklyVisitors): The WeeklyVisitors object (a child of rest_framework.views.APIView).
    request (HTTPRequest): The request object.
    enddate (str): The date string that serves as a starting point for the calculations; in the format '%Y-%m-%d' (see datetime documentation).
    format (str): A format suffix pattern; by saying None, I am accepting a valid HTTP request regardless of whether it is a JSON request or not.

    Returns:
    Response (rest_framework.response.Response): A response object whose Content-Type should always be JSON text.
    """
    def get(self, request, enddate, format=None):
        week_days, numeric_dates = get_dates(enddate, 7)

        weekly_cities = []
        other_counts  = []
        top_counts    = []
        cities_dict = {}

        for i in range(0, 7):
            visitors_by_day = Visitor.objects.filter(
                                day=numeric_dates[i][0], month=numeric_dates[i][1],
                                year=numeric_dates[i][2]    
                            )
            for visitor in visitors_by_day:
                city = visitor.city + ', ' + visitor.region + ', ' + visitor.country
                try:
                    cities_dict[city] += 1
                except: # Initial dictionary entry for region and city
                    cities_dict[city] = 1

        if (len(cities_dict) > 9):
            for key in cities_dict.keys():
                other_counts.append(cities_dict[key])
            
            other_counts.sort(reverse=True)
            top_counts = other_counts[:9]
            other_counts = other_counts[9:]

            ccopy = ''
            for count in top_counts:
                for city in cities_dict:
                    if (cities_dict[city] == count):
                        ccopy = city
                        break
                weekly_cities.append(ccopy)
                del cities_dict[ccopy]

            cities_dict['Other'] = 0
            for count in other_counts:
                cities_dict['Other'] += count
            top_counts.append(cities_dict['Other'])
            weekly_cities.append('Other')

        else:
            for key in cities_dict.keys():
                weekly_cities.append(key)
                top_counts.append(cities_dict[key])

        data = {
            "week_label": week_days[6] + " ⁠— " + week_days[0],
            "city_labels": weekly_cities,
            "counts_per_week": top_counts
        }

        return Response(data)


class MonthlyVisitors(APIView):
    """Aggregates page visits per 30 days from the Visitor model
    per a 30-day period spanning from the date in string enddate to the
    previous 29 days from enddate. Additionally, the function groups
    the visits from the same country and region together and provides
    labels for the count of each city for the top 10 regions. Any views
    from regions that don't make up the top 10 are grouped together under
    the label of 'Other'. Besides all that, the total number of visits,
    the average time of a visit, and the amount of visitors which have
    previously viewed the site are computed over the 30-day duration.

    Parameters:
    self (MonthlyVisitors): The MonthlyVisitors object (a child of rest_framework.views.APIView).
    request (HTTPRequest): The request object.
    enddate (str): The date string that serves as a starting point for the calculations; in the format '%Y-%m-%d' (see datetime documentation).
    format (str): A format suffix pattern; by saying None, I am accepting a valid HTTP request regardless of whether it is a JSON request or not.

    Returns:
    Response (rest_framework.response.Response): A response object whose Content-Type should always be JSON text.
    """
    def get(self, request, enddate, format=None):
        week_days, numeric_dates = get_dates(enddate, 30)

        monthly_regions = []
        monthly_counts = []
        top_counts = []
        regions_dict = {}
        hours = 0
        num_visits = 0

        for i in range(0, 30):
            visitors_by_day = Visitor.objects.filter(
                                day=numeric_dates[i][0], month=numeric_dates[i][1],
                                year=numeric_dates[i][2]
                            )
            for visitor in visitors_by_day:
                num_visits += 1
                hours += (int(visitor.time[:2]))

                region = visitor.region + ', ' + visitor.country
                try:
                    regions_dict[region] += 1
                except: # Initial dictionary entry for region and city
                    regions_dict[region] = 1

        # This will give modulo by zero error if no hours (no visits):
        try:
            hr = ( hours // num_visits )
            if (hr == 12): # Make hour 12-hr format
                hr_str = str(hr) + ' PM'
            elif (hr > 12):
                hr = (hr - 12)
                hr_str = str(hr) + ' PM'
            else:
                hr_str = str(hr) + ' AM'
        except:
            hr_str = 'None'

        if (len(regions_dict) > 9):
            for key in regions_dict.keys():
                monthly_counts.append(regions_dict[key])

            monthly_counts.sort(reverse=True)
            top_counts = monthly_counts[:9]
            monthly_counts = monthly_counts[9:]

            rcopy = ''
            for count in top_counts: # Need to match up top 10 regions with top 10 counts
                for region in regions_dict:
                    if (regions_dict[region] == count):
                        rcopy = region
                        break # Break out of inner for since value was found.
                monthly_regions.append(rcopy)
                del regions_dict[rcopy] # Delete the dict entry now that it has been used.

            # All counts which are not in top 10 will be added to other category:
            regions_dict['Other'] = 1
            for count in monthly_counts:
                regions_dict['Other'] += count
            top_counts.append(regions_dict['Other'])
            monthly_regions.append('Other')
        
        else:
            for key in regions_dict.keys():
                monthly_regions.append(key)
                top_counts.append(regions_dict[key])

        data = {
            "month_label": week_days[27] + " ⁠— " + week_days[0],
            "region_labels": monthly_regions,
            "counts_per_region": top_counts,
            "avg_view_hour": hr_str,
            "total_visits": num_visits,
        }

        return Response(data)


@login_required
def views_charts_today(request):
    """Provides the Views page template for authenticated users
    which uses the current date as its enddate or the start
    of the time period that will be graphed in the template.
    Additionally, the ExportRecords form is provided to the
    template with the table_name pre-populated with 'views'.

    Parameters:
    request (HttpRequest): An HTTP Request object. 

    Returns:
    HttpResponse: Directs the user to the appropriate URL.
    """
    date = dt.now()
    enddate = (str(date.year) + '-' + str(date.month) 
				+ '-' + str(date.day))
    form = ExportRecordsForm(initial={'table_name': 'views'})

    context = { 'enddate': enddate, 'form': form }

    return render(request, 'api/charts/views.html', context)


@login_required
def views_charts_enddate(request, enddate):
    """Provides the Views page template for authenticated
    users which uses the date specified by enddate as the start
    of the time period that will be graphed in the template.
    Additionally, the ExportRecords form is provided to the
    template with the table_name pre-populated with 'views'.

    Parameters:
    request (HttpRequest): An HTTP Request object. 
    enddate (str): The date that begins the time period graphed; in the format ('enddate=2020-08-03').

    Returns:
    HttpResponse: Directs the user to the appropriate URL.
    """
    enddate = enddate.split('=')[0]
    form = ExportRecordsForm(initial={'table_name': 'views'})

    context = { 'enddate': enddate, 'form': form }

    return render(request, 'api/charts/views.html', context)


@login_required
def visitors_charts_today(request):
    """Provides the Visitors page template for authenticated
    users which uses the current date as its enddate or the start
    of the time period that will be graphed in the template.
    Additionally, the ExportRecords form is provided to the
    template with the table_name pre-populated with 'visitors'.

    Parameters:
    request (HttpRequest): An HTTP Request object. 

    Returns:
    HttpResponse: Directs the user to the appropriate URL.
    """
    date = dt.now()
    enddate = (str(date.year) + '-' + str(date.month) 
				+ '-' + str(date.day))
    form = ExportRecordsForm(initial={'table_name': 'visitors'})
        
    context = { 'enddate': enddate, 'form': form }

    return render(request, 'api/charts/visitors.html', context)


@login_required
def visitors_charts_enddate(request, enddate):
    """Provides the Visitors page template for authenticated
    users which uses the date specified by enddate as the start
    of the time period that will be graphed in the template.
    Additionally, the ExportRecords form is provided to the
    template with the table_name pre-populated with 'visitors'.

    Parameters:
    request (HttpRequest): An HTTP Request object. 
    enddate (str): The date that begins the time period graphed; in the format ('endate=2020-08-03').

    Returns:
    HttpResponse: Directs the user to the appropriate URL.
    """
    enddate = enddate.split('=')[0]
    form = ExportRecordsForm(initial={'table_name': 'visitors'})

    context = { 'enddate': enddate, 'form': form }

    return render(request, 'api/charts/visitors.html', context)


@login_required
def export_views(request):
    """If the request method is POST, the db_exporter module is employed
    to export database records of the Page model over the time specified
    in the form and provides a string of the data back to this function
    in the specified format (CSV, JSON, or SQL). The function will respond
    by providing the user with the file download using the file name
    provided in the form.

    Parameters:
    request (HttpRequest): An HTTP Request object.

    Returns:
    HttpResponse: Provides a response containing the file of content_type which is the Content-Type determined by db_exporter.
    """
    if(request.method == 'POST'):
        form = ExportRecordsForm(data=request.POST)
        if (form.is_valid()):
            data, content_type, extension = db_exporter.export_records(form, 'Page')
            filename = form.cleaned_data['file_name'].rsplit('.', 1)[0] + extension

            response = HttpResponse(data, content_type=content_type)
            response['Content-Disposition'] = f"attachment; filename={ filename }"
            return response

    return render(request, 'admin_pages/index.html')


@login_required
def export_visitors(request):
    """If the request method is POST, the db_exporter module is employed
    to export database records of the Visitors model over the time specified
    in the form and provides a string of the data back to this function
    in the specified format (CSV, JSON, or SQL). The function will respond
    by providing the user with the file download using the file name
    provided in the form.

    Parameters:
    request (HttpRequest): An HTTP Request object.

    Returns:
    HttpResponse: Provides a response containing the file of content_type which is the Content-Type determined by db_exporter.
    """
    if (request.method == 'POST'):
        form = ExportRecordsForm(data=request.POST)
        if (form.is_valid()):
            data, content_type, extension = db_exporter.export_records(form, 'Visitor')
            filename = form.cleaned_data['file_name'].rsplit('.', 1)[0] + extension

            response = HttpResponse(data, content_type=content_type)
            response['Content-Disposition'] = f"attachment; filename={ filename }"
            return response

    return render(request, 'admin_pages/index.html')


# JS alert will notify the user of success or failure based on the deletion
# status code.
@login_required
def delete_views(request, time_period, enddate):
    """The delete_records function is employed to delete Page
    records beginning with the date specified in the enddate
    param and deleting all the previous (time_period - 1) days
    from the enddate. This is of course, unless enddate=='0' in
    which case the delete_records function will delete all records.
    If delete_records returns True, a 200 response is returned;
    otherwise, something has gone inexplicably wrong and a 500
    response is returned.

    Parameters:
    request (HttpRequest): An HTTP Request object.
    time_period (str): The time period of View model records to delete.
    enddate (str): The date that begins the time period to delete; in the format ('2020-08-03').

    Returns:
    HttpResponse: Provides a response either of OK (200) or Internal Server Error (500).
    """
    if (delete_records(int(time_period), enddate, 'Page')):
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=500)


@login_required
def delete_visitors(request, time_period, enddate): 
    """The delete_records function is employed to delete Visitor
    records beginning with the date specified in the enddate
    param and deleting all the previous (time_period - 1) days
    from the enddate. This is of course, unless enddate=='0' in
    which case the delete_records function will delete all records.
    If delete_records returns True, a 200 response is returned;
    otherwise, something has gone inexplicably wrong and a 500
    response is returned.

    Parameters:
    request (HttpRequest): An HTTP Request object.
    time_period (str): The time period of Visitor model records to delete.
    enddate (str): The date that begins the time period to delete; in the format ('2020-08-03').

    Returns:
    HttpResponse: Provides a response either of OK (200) or Internal Server Error (500).
    """
    if (delete_records(int(time_period), enddate, 'Visitor')):
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=500)