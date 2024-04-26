from src.scrapers import Scraper


class Spearhead(Scraper):
    def __init__(self, company_name, url, logo_url):
        super().__init__(company_name, url, logo_url)

    def get_jobs(self):
        response = self.get_soup()
        jobs = response.find_all('a', class_='text-decoration-none')

        for job in jobs:
            link = 'https://spearhead.systems' + job.get('href')
            title = job.find('h3').text.strip()

            self.get_jobs_dict(title, link, 'Bucuresti')

        return self.jobs_list


spearhead = Spearhead(
    company_name='spearhead',
    url='https://spearhead.systems/jobs',
    logo_url='https://www.romanianstartups.com/wp-content/uploads/2013/09/spearhead-systems-logo-177x100.jpg',
)
spearhead.get_jobs()
spearhead.push_peviitor()