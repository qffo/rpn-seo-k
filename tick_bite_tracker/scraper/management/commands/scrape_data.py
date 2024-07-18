import random
import sqlite3
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from scraper.models import TickBiteReport


class Command(BaseCommand):
    help = 'Scrape tick bite reports from Rospotrebnadzor'

    def handle(self, *args, **kwargs):
        url = 'https://40.rospotrebnadzor.ru/epidemiologic_situation/'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        articles = soup.find_all('a', text=lambda x: x and x.strip().startswith(
            'О ситуации по иксодовому клещевому боррелиозу'))

        for article in articles:
            link = article['href']
            article_response = requests.get(
                f"https://40.rospotrebnadzor.ru/{link}")
            article_soup = BeautifulSoup(article_response.text, 'html.parser')
            text = article_soup.get_text()

            start_date_str, end_date_str, cases_str = extract_data(text)

            start_date = datetime.strptime(start_date_str, '%d.%m.%Y').date()
            end_date = datetime.strptime(end_date_str, '%d.%m.%Y').date()
            cases = int(cases_str)

            report, created = TickBiteReport.objects.get_or_create(
                start_date=start_date,
                end_date=end_date,
                defaults={'cases': cases},
            )
            if not created:
                report.cases = cases
                report.save()


def extract_data(text):

    if re.search(r'обратилось (\d+) человек', text):
        cases_str = re.search(r'обратилось (\d+) человек', text).group(1)
    elif re.search(r'обратился (\d+) человек', text):
        cases_str = re.search(r'обратился (\d+) человек', text).group(1)
    else:
        cases_str = 0

    matchh = re.search(
        r'в Калужской области за период  с (\d{2}.\d{2}.\d{4}) г. по', text)
    if matchh:
        start_date_str = matchh.group(1)
    else:
        start_date_str = f"{random.randint(1,30)}.{random.randint(1,12)}.2024"

    matchhh = re.search(
        r'по (\d{2}.\d{2}.\d{4}) г.', text)
    if matchhh:
        end_date_str = matchhh.group(1)
    else:
        end_date_str = f"{random.randint(1,30)}.{random.randint(1,12)}.2024"

    print(cases_str, start_date_str, end_date_str)

    return start_date_str, end_date_str, cases_str
