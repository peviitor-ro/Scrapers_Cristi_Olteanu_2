from src.scrapers import Scraper


class Mindspace(Scraper):
    def __init__(self, company_name, url, logo_url):
        super().__init__(company_name, url, logo_url)

    def get_jobs(self):
        jobs = self.get_soup().find_all('a', class_='career-item w-inline-block active')
        for job in jobs:
            title = job.find('h3', class_='career-tab-title-2').text
            link = job.get('href')
            city = 'Bucuresti' if 'Bucharest' in job.find('p', class_='career-tab-text-2').text else None
            if city is not None:
                self.get_jobs_dict(title, link, city)
        return self.jobs_list


mindpspace = Mindspace(
    company_name='Mindspace',
    url='https://www.mindspace.me/careers/#opportunities',
    logo_url=''
)
mindpspace.get_jobs()
mindpspace.push_peviitor()