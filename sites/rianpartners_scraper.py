import re
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from src.scrapers import Scraper


class Rian(Scraper):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.session = requests.Session()

    def fetch(self, url, **kwargs):
        kwargs.setdefault('timeout', 30)
        for attempt in range(3):
            try:
                return self.session.get(url, **kwargs)
            except requests.RequestException:
                if attempt == 2:
                    raise

    def get_link_soup(self, link, params=None, headers=None):
        headers = self.headers if headers is None else headers
        challenge_headers = dict(headers)
        challenge_headers['Referer'] = link
        challenge_headers['Upgrade-Insecure-Requests'] = '1'

        for attempt in range(3):
            response = self.fetch(link, headers=headers, params=params)
            if 'Please wait while your request is being verified' not in response.text:
                break

            verification = self.get_verification(response.text)
            self.fetch(
                urljoin(link, verification['endpoint']),
                params=verification['params'],
                headers=challenge_headers,
                allow_redirects=False,
            )
            response = self.fetch(link, headers=challenge_headers, params=params)
            if 'Please wait while your request is being verified' not in response.text:
                break
            time.sleep(attempt + 1)

        return BeautifulSoup(response.text, 'lxml')

    def get_verification(self, html):
        ts = re.search(r"\['append'\]\('ts','(\d+)'\)", html).group(1)
        endpoint = re.search(r"R='(/[^']+)'", html).group(1)
        pdata = re.search(r"Q='([^']+)'", html).group(1)
        first = re.search(r",m=(.+?),V=", html).group(1)
        second = re.search(r"\),I=(.+?),M=", html).group(1)

        return {
            'endpoint': endpoint,
            'params': {
                'id': '7fa3b767c460b54a2be4d49030b349c7',
                'ts': ts,
                'wsidchk': str(self.js_sum(first) + self.js_sum(second)),
                'pdata': pdata,
                'cttl': '0',
            },
        }

    @staticmethod
    def js_string(value):
        if value is True:
            return 'true'
        if value is False:
            return 'false'
        return str(value)

    @classmethod
    def js_add(cls, left, right):
        if isinstance(left, str) or isinstance(right, str):
            return cls.js_string(left) + cls.js_string(right)
        return left + right

    @classmethod
    def js_sum(cls, expression):
        tokens = []
        position = 0

        while position < len(expression):
            for pattern, value in (('+!+[]', 1), ('+![]', 0), ('!![]', True)):
                if expression.startswith(pattern, position):
                    tokens.append(('value', value))
                    position += len(pattern)
                    break
            else:
                if expression.startswith('+[]', position):
                    tokens.extend((('+', None), ('value', '')))
                    position += 3
                elif expression[position] in '()+':
                    tokens.append((expression[position], None))
                    position += 1
                else:
                    position += 1

        index = 0

        def parse_term():
            nonlocal index
            if (tokens[index][0] == '+' and index + 1 < len(tokens)
                    and tokens[index + 1][0] == '('):
                index += 1
                return int(parse_term())
            if tokens[index][0] == '(':
                index += 1
                value = parse_expression()
                index += 1
                return value
            value = tokens[index][1]
            index += 1
            return value

        def parse_expression():
            nonlocal index
            value = parse_term()
            while index < len(tokens) and tokens[index][0] == '+':
                index += 1
                value = cls.js_add(value, parse_term())
            return value

        return int(parse_expression())

    def get_jobs(self):
        urls = ['https://rian-partners.com/en/rian-partners-jobs-pitesti-jobs-in-production/',
                'https://rian-partners.com/en/careers/']
        for url in urls:
            response = self.get_link_soup(url)
            jobs = response.find_all('tr')

            for job in jobs:
                info = job.find('td')
                if info is not None:
                    title = job.find('td').text.title()
                    link = job.find('a')['href']
                    base_location = job.find('td', class_='location').text
                    city = base_location.split(',')[0].title()
                    county = base_location.split(',')[-1].title().strip('County').strip() if 'county' in base_location.lower() else None

                    self.get_jobs_dict(title, link, city, county=county)
        print(len(self.jobs_list))
        return self.jobs_list


rian = Rian(
    url='https://rian-partners.com/en/careers/',
    company_name='rianpartners',
    logo_url='https://rian-partners.com/wp-content/uploads/2019/09/RIAN-partners-1.png'

)
rian.get_jobs()
rian.push_peviitor()
