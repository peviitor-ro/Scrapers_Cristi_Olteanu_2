import json
import re
import time

import requests as std_requests
from bs4 import BeautifulSoup
from curl_cffi import requests

from src.scrapers import Scraper


class Ness(Scraper):

    MAX_ATTEMPTS = 3
    PUSH_ATTEMPTS = 5
    RETRY_DELAY = 2
    IMPERSONATES = ('firefox133', 'firefox135', 'chrome131', 'chrome120', 'safari17_0')
    SEARCH_URLS = (
        'https://ness-usa.ttcportals.com/search/jobs/in/country/romania',
        'https://ness-usa.ttcportals.com/search/jobs',
    )

    def get_page_soup(self, url, page):
        # the site sits behind a Cloudflare managed challenge that is only
        # issued intermittently; retry until a real, unchallenged page lands
        for _ in range(self.MAX_ATTEMPTS):
            for impersonate in self.IMPERSONATES:
                try:
                    session = requests.Session(impersonate=impersonate)
                    response = session.get(url, params={'page': page}, timeout=30)
                    if response.status_code == 200 and 'Just a moment' not in response.text:
                        return BeautifulSoup(response.text, 'lxml')
                except Exception:
                    pass
            time.sleep(self.RETRY_DELAY)
        return None

    def get_jobs_from_jina(self):
        page = 1
        seen = set()

        while True:
            url = f'https://r.jina.ai/https://ness-usa.ttcportals.com/search/jobs/in/country/romania?page={page}'
            try:
                response = std_requests.get(url, timeout=30)
                if response.status_code != 200:
                    break
            except Exception:
                break

            text = response.text
            pattern = r'## \[(.*?)\]\((https://ness-usa\.ttcportals\.com/jobs/[^\)]+)\).*?Location:\s*(.*?)\n'
            matches = list(re.finditer(pattern, text, re.S))
            if not matches:
                break

            new_jobs = 0
            for match in matches:
                title = match.group(1).strip()
                link = match.group(2).strip()
                location = ' '.join(match.group(3).split())
                if 'Romania' not in location:
                    continue
                if link in seen:
                    continue
                seen.add(link)
                city = 'Romania' if location == 'Romania' else location.split(',')[0].strip().rstrip('.')
                city = self.get_validated_city(city)
                self.get_jobs_dict(title, link, city)
                new_jobs += 1

            if new_jobs == 0:
                break
            page += 1

        return self.jobs_list

    def get_jobs(self):
        for url in self.SEARCH_URLS:
            page = 1
            seen = set()

            while True:
                soup = self.get_page_soup(url, page)
                if soup is None:
                    break

                jobs = soup.find_all('div', class_='jobs-section__item padded-v-small')
                if not jobs:
                    break

                for job in jobs:
                    text = job.get_text(' ', strip=True)
                    if url.endswith('/search/jobs') and 'Romania' not in text:
                        continue

                    title = job.find('a').text.strip()
                    link = job.find('a')['href']
                    location_text = job.find('div', class_='large-4 columns').text.split('Location:')[-1].strip()
                    if location_text == 'Romania':
                        city = 'Romania'
                    else:
                        city = location_text.split(',')[0].strip().rstrip('.')
                    city = self.get_validated_city(city)

                    if link in seen:
                        continue
                    seen.add(link)
                    self.get_jobs_dict(title, link, city)

                page += 1

            if self.jobs_list:
                break

        if not self.jobs_list:
            self.get_jobs_from_jina()

        return self.jobs_list

ness = Ness(
    company_name='ness',
    url='https://ness-usa.ttcportals.com/search/jobs/in/country/romania',
    logo_url='https://ness-usa.ttcportals.com/system/production/assets/357234/original/Ness--logo.png'
)


def push_jobs():
    for _ in range(ness.PUSH_ATTEMPTS):
        try:
            ness.push_peviitor()
            return
        except Exception:
            time.sleep(ness.RETRY_DELAY)
    print(json.dumps(ness.jobs_list, indent=4))


ness.get_jobs()
push_jobs()
