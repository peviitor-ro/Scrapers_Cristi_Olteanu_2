import time

from bs4 import BeautifulSoup
from curl_cffi import requests

from src.scrapers import Scraper


class Ness(Scraper):

    MAX_ATTEMPTS = 10
    RETRY_DELAY = 2

    def get_page_soup(self, session, page):
        # the site sits behind a Cloudflare managed challenge that is only
        # issued intermittently; retry until a real, unchallenged page lands
        for _ in range(self.MAX_ATTEMPTS):
            try:
                response = session.get(f'{self.url}?page={page}', timeout=30)
                if response.status_code == 200 and 'Just a moment' not in response.text:
                    return BeautifulSoup(response.text, 'lxml')
            except Exception:
                pass
            time.sleep(self.RETRY_DELAY)
        return None

    def get_jobs(self):
        page = 1
        session = requests.Session(impersonate='firefox133')

        while True:
            soup = self.get_page_soup(session, page)
            if soup is None:
                break

            jobs = soup.find_all('div', class_='jobs-section__item padded-v-small')

            if len(jobs) > 0:
                for job in jobs:
                    title = job.find('a').text.strip()
                    link = job.find('a')['href']
                    city = job.find('div', class_='large-4 columns').text.split('Location:')[-1].split(',')[0].strip().rstrip('.')
                    city = self.get_validated_city(city)
                    self.get_jobs_dict(title, link, city)

                page += 1
            else:
                break

        return self.jobs_list

ness = Ness(
    company_name='ness',
    url='https://ness-usa.ttcportals.com/search/jobs/in/country/romania',
    logo_url='https://ness-usa.ttcportals.com/system/production/assets/357234/original/Ness--logo.png'
)
ness.get_jobs()
ness.push_peviitor()
