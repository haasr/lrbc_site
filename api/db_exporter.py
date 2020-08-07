from site_pages.models import Page, Visitor
from datetime import datetime as dt, timedelta


def export_csv(model, time_period, enddate):
    """Compiles a string of CSV data that represents the model's (specified
    by the model param) database entries for the given time period
    specified by the date string, enddate and the previous ( time_period
    - 1 ) days (unless time_period's value is 0 which indicates that all
    database entries should be included in the CSV data).

    Parameters:
    model (str): The name of the database model from which to compile the data.
    time_period (int): The number of days including enddate and the previous (time_period - 1) days from enddate for which data will be copied.
    
    Returns:
    data (str): A string of the CSV data.
    """
    if (model == 'Page'):
        value_label = 'page_name, year, month, day, time'
    else:
        value_label = ('ip, city, region, country, year, ' +
                        'month, day, time, prev_visit')

    data = value_label + '\n'

    
    if (time_period == 0):
        if (model == 'Page'):
            collection = Page.objects.all()
        else:
            collection = Visitor.objects.all()
        for item in collection:
            data += item.csv() + '\n'
    else:
        now = dt.strptime(enddate, '%Y-%m-%d')
        now_str = now.__str__().split(' ')[0].split('-')

        if (model == 'Page'):
            for i in range(0, time_period):
                collection = Page.objects.filter(year=now_str[0], 
                                month=now_str[1], day=now_str[2])
                for item in collection:
                    data += item.csv() + '\n'
    
                now = now - timedelta(days=1)
                now_str = now.__str__().split(' ')[0].split('-')
        else:
            for i in range(0, time_period):
                collection = Visitor.objects.filter(year=now_str[0],
                                month=now_str[1], day=now_str[2])
                for item in collection:
                    data += item.csv() + '\n'

                now = now - timedelta(days=1)
                now_str = now.__str__().split(' ')[0].split('-')
    
    return data


def export_json(model, time_period, enddate):
    """Compiles a string of JSON data in the form of a MongoDB-importable 
    collection that represents the model's (specified by the model param)
    database entries for the given time period specified by the date string,
    enddate and the previous ( time_period - 1 ) days (unless time_period's
    value is 0 which indicates that all database entries should be included 
    in the JSON data).

    Parameters:
    model (str): The name of the database model from which to compile the data.
    time_period (int): The number of days including enddate and the previous (time_period - 1) days from enddate for which data will be copied.
    
    Returns:
    data (str): A string of the JSON collection.
    """
    data = ''

    if (time_period == 0):
        if (model == 'Page'):
            collection = Page.objects.all()
        else:
            collection = Visitor.objects.all()
        for item in collection:
            data += item.json() + '\n'
    else:
        now = dt.strptime(enddate, '%Y-%m-%d')
        now_str = now.__str__().split(' ')[0].split('-')

        if (model == 'Page'):
            for i in range(0, time_period):
                collection = Page.objects.filter(year=now_str[0], 
                                month=now_str[1], day=now_str[2])
                for item in collection:
                    data += item.json() + '\n'

                now = now - timedelta(days=1)
                now_str = now.__str__().split(' ')[0].split('-')
        else:
            for i in range(0, time_period):
                collection = Visitor.objects.filter(year=now_str[0],
                                month=now_str[1], day=now_str[2])
                for item in collection:
                    data += item.json() + '\n'

                now = now - timedelta(days=1)
                now_str = now.__str__().split(' ')[0].split('-')

    return data


def export_sql(model, table_name, time_period, enddate):
    """Compiles a string of SQL data in the form of a SQL insert statments
    that represents the model's (specified by the model param) database
    entries for the given time period specified by the date string,
    enddate and the previous ( time_period - 1 ) days (unless time_period's
    value is 0 which indicates that all database entries should be included 
    in the JSON data).

    Parameters:
    model (str): The name of the database model from which to compile the data.
    time_period (int): The number of days including enddate and the previous (time_period - 1) days from enddate for which data will be copied.
    
    Returns:
    data (str): A string of the SQL inserts data.
    """
    if (model == 'Page'):
        value_label = ('INSERT INTO ' + table_name +
                        ' (page_name, year, month, day, time)')
    else:
        value_label = ('INSERT INTO ' + table_name + ' (ip, city, ' +
                        'region, country, year, month, day, time, ' +
                        'prev_visit)')

    data = ''
    
    if (time_period == 0):
        if (model == 'Page'):
            collection = Page.objects.all()
        else:
            collection = Visitor.objects.all()
        for item in collection:
            data += value_label + ' VALUES (' + item.sql() + ');\n'
    else:
        now = dt.strptime(enddate, '%Y-%m-%d')
        now_str = now.__str__().split(' ')[0].split('-')

        if (model == 'Page'):
            for i in range(0, time_period):
                collection = Page.objects.filter(year=now_str[0], 
                                month=now_str[1], day=now_str[2])
                for item in collection:
                    data += value_label + ' VALUES (' + item.sql() + ');\n'

                now = now - timedelta(days=1)
                now_str = now.__str__().split(' ')[0].split('-')
        else:
            for i in range(0, time_period):
                collection = Visitor.objects.filter(year=now_str[0],
                                month=now_str[1], day=now_str[2])
                for item in collection:
                    data += value_label + ' VALUES (' + item.sql() + ');\n'

                now = now - timedelta(days=1)
                now_str = now.__str__().split(' ')[0].split('-')

    return data


def export_records(form, model):
    """Creates the file data and decides the Content-Type and file
    extension of the data based on the ExportRecordForm's 'export_type'
    value all of which is returned to the caller.

    Parameters:
    form (ExportRecordForm): The form from which to derive the data needed to create a file of the requested data.
    model (str): The name of the database model from which to export the records.

    Returns:
    data (str): The string of data
    content_type (str): The assigned Content-Type for the data -- either 'text/csv', 'application/json', or 'application/sql'.
    extension (str): The assigned extension for the file to be created from the data -- either '.csv', '.json', or '.sql'.
    """
    data = form.cleaned_data
    if (data['export_type'] == 'CSV'):
        data = export_csv(model, data['time_period'], data['end_date'])
        content_type = 'text/csv'
        extension = '.csv'
    elif (data['export_type'] == 'JSON'):
        data = export_json(model, data['time_period'], data['end_date'])
        content_type = 'application/json'
        extension = '.json'
    else: # Else, SQL inserts
        data = export_sql(model, data['table_name'], data['time_period'],
                    data['end_date'])
        content_type = 'application/sql'
        extension = '.sql'
        
    return data, content_type, extension