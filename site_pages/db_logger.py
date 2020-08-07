from .models import Page, Visitor
from ip2geotools.databases.noncommercial import DbIpCity
from lrbc_site import settings
from admin_pages.models import NoLogIPModel
import json
import os
import re
import socket

class DBLogger:

    BOT_FILE_PATH = settings.BASE_DIR + '/site_pages/data/crawler-user-agents.json'
    USER_AGENTS_JSON = None
    nolog_ip_list = []

    # Assume DNS containing any of these strings is a bot:
    URL_BOTS_LIST = [
        'amazonaws',
        'census',
        'crawl',
        'fbsb.net',
        'scan',
        'security',
        '.crawl.baidu.com',
        '.crawl.baidu.jp',
        '.search.msn.com',
        '.google.com',
        '.googlebot.com',
        '.crawl.yahoo.net',
        '.yandex.ru',
        '.yandex.net',
        '.yandex.com'
    ]

    def __init__(self):
        """On initialization, self.USER_AGENTS_JSON is populated with the JSON
        file stored at self.BOT_FILE_PATH. Additionally the refresh_nolog_ip_list
        function is called to create a flattened list of the IP addresses of all
        NoLogIPModel objects.

        Parameters:
        self (DBLogger): The initialized DBLogger instance.
        """
        json_file = open(self.BOT_FILE_PATH, 'r')
        self.USER_AGENTS_JSON = json.load(json_file)
        json_file.close()

        self.refresh_nolog_ip_list()


    def refresh_nolog_ip_list(self):
        """Stores a flattened list of the IP addresses of all NoLogIPModel objects.

        Parameters:
        self (DBLogger): The initialized DBLogger instance.
        """
        self.nolog_ip_list = NoLogIPModel.objects.all().values_list('ip', flat=True)

    
    def log_ip(self, ip_address):
        """Matches the ip_address param value against each address in self.nolog_ip_list.
        If it does not match any address, True is returned; otherwise false.

        Parameters:
        self (DBLogger): The initialized DBLogger instance.
        ip_address (str): An IP address to be matched against each address in self.nolog_ip_list.

        Returns: bool:True if no match was found; False otherwise.
        """
        log_ip = True
        for ip in self.nolog_ip_list:
            if (ip == ip_address):
                log_ip = False
                break
        return log_ip


    def ip_is_bot(self, ip_address):
        """Performs a DNS lookup of the IP address. Each string in
        self.URL_BOTS_LIST is then checked to see if the hostname
        contains it, if so, the IP is considered to be from a bot's
        IP and True is returned. Otherwise False is returned.

        Parameters:
        self (DBLogger): The initialized DBLogger instance.
        ip_address (str): An IP address to lookup a hostname for.

        Returns: 
        match (bool): False if no match was found; True otherwise.
        """
        match = False
        try:
            hostname = socket.gethostbyaddr(ip_address)[0]
            for line in self.URL_BOTS_LIST:
                if line in hostname:
                    match = True
                    break
        except:
            pass
        return match


    def agent_is_bot(self, user_agent):
        """Matches the User-Agent string stored in the user_agent param 
        against each User-Agent string instance in USER_AGENTS_JSON.
        If no match is found False is returned; else True is returned.

        Parameters:
        self (DBLogger): The initialized DBLogger instance.
        user_agent (str): A User-Agent string to check whether it appears to be a bot or not.

        Returns:
        match (bool): False if no match was found; True otherwise.
        """
        match = False
        for entry in self.USER_AGENTS_JSON:
            for instance in entry['instances']:
                if (user_agent==instance):
                    match = True
                    break
        return match


    def log_visitor(self, ip_address, user_agent, datetime):
        """Uses the log_ip, ip_is_bot, and agent_is_bot to qualify that the
        entry is not a bot before logging a new Visitor. To log a new Visitor,
        the ip2geotools.databases.noncommercial.DbIPCity module is employeed
        to acquire the city, region, and country of the IP address.
        The date and time are also derived from the datetime string
        and if the IP address is found in an existing database record,
        the previous visit date is recorded in the new Visitor object as well.

        Parameters:
        self (DBLogger): The initialized DBLogger instance.
        ip_address (str): An IP address to be matched against each address in self.nolog_ip_list.
        user_agent (str): A User-Agent string to check whether it appears to be a bot or not.
        datetime (str): A timestamp in the format, '%Y-%m-%d %H:%M:%S' (see datetime documentation).
        """
        if (self.log_ip(ip_address)):
            if not (self.ip_is_bot(ip_address)):
                if not(self.agent_is_bot(user_agent)):
                    try:
                        resp = DbIpCity.get(ip_address, api_key='free')
                        dt_split = datetime.split(' ')
                        date_split = dt_split[0].split('-') # Split yyyy-mm-dd into { yyyy, mm, dd }

                        prev_visit = ''
                        visitor_qset = Visitor.objects.filter(ip=ip_address)
                        if(len(visitor_qset) > 0): # If this ip has been logged before, store prev_visit date
                            visitor = visitor_qset[0]
                            prev_visit = (visitor.year + '-' + visitor.month 
                                            + '-' + visitor.day)

                        visitor = Visitor(
                            ip=ip_address,
                            city=resp.city,
                            region=resp.region,
                            country=resp.country,
                            year=date_split[0],
                            month=date_split[1],
                            day=date_split[2],
                            time=dt_split[1],
                            prev_visit=prev_visit
                        )
                        visitor.save()
                    except Exception as e:
                        pass


    def log_page(self, ip_address, user_agent, page_name, datetime):
        """Uses the log_ip, ip_is_bot, and agent_is_bot to qualify that the
        entry is not a bot before logging a new Page. To log a new Page,
        the date and time are also derived from the datetime string.

        Parameters:
        self (DBLogger): The initialized DBLogger instance.
        ip_address (str): An IP address to be matched against each address in self.nolog_ip_list.
        user_agent (str): A User-Agent string to check whether it appears to be a bot or not.
        page_name (str): The name of the page being logged.
        datetime (str): A timestamp in the format, '%Y-%m-%d %H:%M:%S' (see datetime documentation).
        """
        if (self.log_ip(ip_address)):
            if not(self.ip_is_bot(ip_address)):
                if not(self.agent_is_bot(user_agent)):
                    dt_split = datetime.split(' ')
                    date_split = dt_split[0].split('-') # Split yyyy-mm-dd into { yyyy, mm, dd }
                    page = Page(
                        page_name=page_name,
                        year=date_split[0],
                        month=date_split[1],
                        day=date_split[2],
                        time=dt_split[1]
                    )
                    page.save()
from .models import Page, Visitor
from ip2geotools.databases.noncommercial import DbIpCity
from lrbc_site import settings
from admin_pages.models import NoLogIPModel
import json
import os
import re
import socket

class DBLogger:

    BOT_FILE_PATH = settings.BASE_DIR + '/site_pages/data/crawler-user-agents.json'
    USER_AGENTS_JSON = None
    nolog_ip_list = []

    # Assume DNS containing any of these strings is a bot:
    URL_BOTS_LIST = [
        'amazonaws',
        'census',
        'crawl',
        'fbsb.net',
        'scan',
        'security',
        '.crawl.baidu.com',
        '.crawl.baidu.jp',
        '.search.msn.com',
        '.google.com',
        '.googlebot.com',
        '.crawl.yahoo.net',
        '.yandex.ru',
        '.yandex.net',
        '.yandex.com'
    ]

    def __init__(self):
        """On initialization, self.USER_AGENTS_JSON is populated with the JSON
        file stored at self.BOT_FILE_PATH. Additionally the refresh_nolog_ip_list
        function is called to create a flattened list of the IP addresses of all
        NoLogIPModel objects.

        Parameters:
        self (DBLogger): The initialized DBLogger instance.
        """
        json_file = open(self.BOT_FILE_PATH, 'r')
        self.USER_AGENTS_JSON = json.load(json_file)
        json_file.close()

        self.refresh_nolog_ip_list()


    def refresh_nolog_ip_list(self):
        """Stores a flattened list of the IP addresses of all NoLogIPModel objects.

        Parameters:
        self (DBLogger): The initialized DBLogger instance.
        """
        self.nolog_ip_list = NoLogIPModel.objects.all().values_list('ip', flat=True)

    
    def log_ip(self, ip_address):
        """Matches the ip_address param value against each address in self.nolog_ip_list.
        If it does not match any address, True is returned; otherwise false.

        Parameters:
        self (DBLogger): The initialized DBLogger instance.
        ip_address (str): An IP address to be matched against each address in self.nolog_ip_list.

        Returns: bool:True if no match was found; False otherwise.
        """
        log_ip = True
        for ip in self.nolog_ip_list:
            if (ip == ip_address):
                log_ip = False
                break
        return log_ip


    def ip_is_bot(self, ip_address):
        """Performs a DNS lookup of the IP address. Each string in
        self.URL_BOTS_LIST is then checked to see if the hostname
        contains it, if so, the IP is considered to be from a bot's
        IP and True is returned. Otherwise False is returned.

        Parameters:
        self (DBLogger): The initialized DBLogger instance.
        ip_address (str): An IP address to lookup a hostname for.

        Returns: 
        match (bool): False if no match was found; True otherwise.
        """
        match = False
        try:
            hostname = socket.gethostbyaddr(ip_address)[0]
            for line in self.URL_BOTS_LIST:
                if line in hostname:
                    match = True
                    break
        except:
            pass
        return match


    def agent_is_bot(self, user_agent):
        """Matches the User-Agent string stored in the user_agent param 
        against each User-Agent string instance in USER_AGENTS_JSON.
        If no match is found False is returned; else True is returned.

        Parameters:
        self (DBLogger): The initialized DBLogger instance.
        user_agent (str): A User-Agent string to check whether it appears to be a bot or not.

        Returns:
        match (bool): False if no match was found; True otherwise.
        """
        match = False
        for entry in self.USER_AGENTS_JSON:
            for instance in entry['instances']:
                if (user_agent==instance):
                    match = True
                    break
        return match


    def log_visitor(self, ip_address, user_agent, datetime):
        """Uses the log_ip, ip_is_bot, and agent_is_bot to qualify that the
        entry is not a bot before logging a new Visitor. To log a new Visitor,
        the ip2geotools.databases.noncommercial.DbIPCity module is employeed
        to acquire the city, region, and country of the IP address.
        The date and time are also derived from the datetime string
        and if the IP address is found in an existing database record,
        the previous visit date is recorded in the new Visitor object as well.

        Parameters:
        self (DBLogger): The initialized DBLogger instance.
        ip_address (str): An IP address to be matched against each address in self.nolog_ip_list.
        user_agent (str): A User-Agent string to check whether it appears to be a bot or not.
        datetime (str): A timestamp in the format, '%Y-%m-%d %H:%M:%S' (see datetime documentation).
        """
        if (self.log_ip(ip_address)):
            if not (self.ip_is_bot(ip_address)):
                if not(self.agent_is_bot(user_agent)):
                    try:
                        resp = DbIpCity.get(ip_address, api_key='free')
                        dt_split = datetime.split(' ')
                        date_split = dt_split[0].split('-') # Split yyyy-mm-dd into { yyyy, mm, dd }

                        prev_visit = ''
                        visitor_qset = Visitor.objects.filter(ip=ip_address)
                        if(len(visitor_qset) > 0): # If this ip has been logged before, store prev_visit date
                            visitor = visitor_qset[0]
                            prev_visit = (visitor.year + '-' + visitor.month 
                                            + '-' + visitor.day)

                        visitor = Visitor(
                            ip=ip_address,
                            city=resp.city,
                            region=resp.region,
                            country=resp.country,
                            year=date_split[0],
                            month=date_split[1],
                            day=date_split[2],
                            time=dt_split[1],
                            prev_visit=prev_visit
                        )
                        visitor.save()
                    except Exception as e:
                        pass


    def log_page(self, ip_address, user_agent, page_name, datetime):
        """Uses the log_ip, ip_is_bot, and agent_is_bot to qualify that the
        entry is not a bot before logging a new Page. To log a new Page,
        the date and time are also derived from the datetime string.

        Parameters:
        self (DBLogger): The initialized DBLogger instance.
        ip_address (str): An IP address to be matched against each address in self.nolog_ip_list.
        user_agent (str): A User-Agent string to check whether it appears to be a bot or not.
        page_name (str): The name of the page being logged.
        datetime (str): A timestamp in the format, '%Y-%m-%d %H:%M:%S' (see datetime documentation).
        """
        if (self.log_ip(ip_address)):
            if not(self.ip_is_bot(ip_address)):
                if not(self.agent_is_bot(user_agent)):
                    dt_split = datetime.split(' ')
                    date_split = dt_split[0].split('-') # Split yyyy-mm-dd into { yyyy, mm, dd }
                    page = Page(
                        page_name=page_name,
                        year=date_split[0],
                        month=date_split[1],
                        day=date_split[2],
                        time=dt_split[1]
                    )
                    page.save()
