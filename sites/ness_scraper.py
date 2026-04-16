import cloudscraper

from src.scrapers import Scraper


class Ness(Scraper):

    def get_jobs(self):
        page = 1
        flag = True
        scraper = cloudscraper.create_scraper(
    browser={
        'browser': 'chrome',
        'platform': 'windows',
        'mobile': False
    }
)
        
        while flag:

            response = scraper.get(f'https://ness-usa.ttcportals.com/search/jobs/in/country/romania?page={page}', timeout=30)
            soup = self.soup(response.text)
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
                flag = False

        return self.jobs_list

    @staticmethod
    def soup(html):
        from bs4 import BeautifulSoup
        return BeautifulSoup(html, 'lxml')

ness = Ness(
    company_name='ness',
    url='https://ness-usa.ttcportals.com/search/jobs/in/country/romania',
    logo_url='https://ness-usa.ttcportals.com/system/production/assets/357234/original/Ness--logo.png'
)
ness.get_jobs()
ness.push_peviitor()
