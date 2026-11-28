import re
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from src.scrapers import Scraper


class Interratravel(Scraper):

    def fetch(self, session, url, **kwargs):
        kwargs.setdefault('timeout', 30)
        for attempt in range(3):
            try:
                return session.get(url, **kwargs)
            except requests.RequestException:
                if attempt == 2:
                    raise

    def get_soup(self, params=None, headers=None, **kwargs):
        headers = self.headers if headers is None else headers
        session = requests.Session()
        challenge_headers = dict(headers)
        challenge_headers['Referer'] = self.url
        challenge_headers['Upgrade-Insecure-Requests'] = '1'

        for attempt in range(3):
            response = self.fetch(session, self.url, headers=headers, params=params, **kwargs)
            if 'Please wait while your request is being verified' not in response.text:
                break

            verification = self.get_verification(response.text)
            response = self.fetch(
                session,
                urljoin(self.url, verification['endpoint']),
                params=verification['params'],
                headers=challenge_headers,
                allow_redirects=False,
            )
            response = self.fetch(session, self.url, headers=challenge_headers)
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
        jobs = self.get_soup().find_all('div', class_='col-md-7 col-lg-8 align-self-center')

        for job in jobs:
            title = job.find('h2').text
            link = job.find('a')['href']

            self.get_jobs_dict(title, link, 'Bucuresti')


interratravel = Interratravel(
    company_name='InterraTravel',
    url='https://www.interra.ro/angajari/',
    logo_url=''
)
interratravel.get_jobs()
interratravel.push_peviitor()
