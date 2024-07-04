from src.county import get_county
from src.scrapers import Scraper


class Prohuman(Scraper):
    def __init__(self, company_name, url, logo_url):
        super().__init__(company_name, url, logo_url)

    def get_jobs(self):

        response = self.get_json()

        for job in response:
            title = job['title']
            link = 'https://www.prohuman.ro/candidati/jobs/' + job['slug']
            cities = [city['location'] for city in job['jobs_job_locations'] if get_county(city['location']) is not None]

            if len(cities) > 0:
                self.get_jobs_dict(title, link, cities)

        return self.jobs_list

prohuman = Prohuman(
    company_name='prohuman',
    url='https://www.prohuman.ro/api/getAllJobs',
    logo_url='https://www.prohuman.ro/wp-content/uploads/2018/02/Logo-Prohuman-650x105.png'
)
prohuman.get_jobs()
prohuman.push_peviitor()