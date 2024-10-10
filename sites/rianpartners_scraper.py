from src.county import get_county
from src.scrapers import Scraper


class Rian(Scraper):

    def get_jobs(self):
        response = self.get_soup()
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

        return self.jobs_list

rian = Rian(
    url='https://rian-partners.com/en/careers/',
    company_name='rianpartners',
    logo_url='https://rian-partners.com/wp-content/uploads/2019/09/RIAN-partners-1.png'

)
rian.get_jobs()
rian.push_peviitor()

