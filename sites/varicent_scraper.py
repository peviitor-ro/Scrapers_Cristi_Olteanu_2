from src.scrapers import Scraper


class VaricentScraper(Scraper):

    def __init__(self, company_name, url, logo_url):
        super().__init__(company_name, url, logo_url)

    def get_jobs(self):

        jobs = self.get_soup().find_all('div', class_='posting')

        for job in jobs:
            title = job.find('h5', attrs={'data-qa': 'posting-name'}).text
            info = job.find('span', attrs={'class': 'display-inline-block small-category-label workplaceTypes'}).text
            link = job.find('a').get('href')

            if 'remote' in info.lower():
                job_type = 'remote'
            elif 'Hybrid' in info.lower():
                job_type = 'hybrid'
            else:
                job_type = 'on-site'

            self.get_jobs_dict(title, link, 'Bucuresti', job_type)

        return self.jobs_list


varicent = VaricentScraper(
    company_name='varicent',
    url='https://jobs.lever.co/varicent?location=Bucharest',
    logo_url=''
)
varicent.get_jobs()
varicent.push_peviitor()


