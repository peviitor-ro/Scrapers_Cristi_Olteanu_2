from src.scrapers import Scraper


class Interratravel(Scraper):
    def __init__(self, company_name, url, logo_url):
        super().__init__(company_name, url, logo_url)

    def get_jobs(self):
        jobs = self.get_soup().find_all('div', class_='col-md-7 col-lg-8 align-self-center')

        for job in jobs:
            title = job.find('h2').text
            link = job.find('a')['href']

            self.get_jobs_dict(title,link,'Bucuresti')


interratravel = Interratravel(
    company_name='InterraTravel',
    url='https://www.interra.ro/angajari/',
    logo_url=''
)
interratravel.get_jobs()
interratravel.push_peviitor()

