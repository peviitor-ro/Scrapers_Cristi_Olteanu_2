from src.county import get_county
from src.scrapers import Scraper


class Rian(Scraper):
    def __init__(self, company_name, url, logo_url):
        super().__init__(company_name, url, logo_url)

    def get_jobs(self):
        response = self.get_soup()
        jobs = response.find_all('tr')

        for job in jobs:
            info = job.find('td')
            if info is not None:
                title = job.find('td').text
                link = job.find('a')['href']
                city = job.find('td', class_='location').text.split(',')[0].split('/')

                for i in range(len(city)):
                    city[i] = self.get_validated_city(str(city[i].strip()).lower())

                self.get_jobs_dict(title, link, city)

        return self.jobs_list

rian = Rian(
    url='https://rian-partners.com/en/careers/',
    company_name='rianpartners',
    logo_url='https://rian-partners.com/wp-content/uploads/2019/09/RIAN-partners-1.png'

)
rian.get_jobs()
rian.push_peviitor()