import requests

from src.scrapers import Scraper


class ExeSoftware(Scraper):
    def __init__(self, company_name, url, logo_url):
        super().__init__(company_name, url, logo_url)

    def get_jobs(self):
        response = self.get_soup()
        jobs = response.find_all('div', class_='uncont')

        for job in jobs:
            info_link = job.find('a')

            if info_link:
                link = info_link.get('href') if 'jobs' in info_link.get('href') else None

                if link:
                    title = job.find('h5').text

                    if requests.get(link).status_code == 200:
                        text = job.find('div', class_='wpb_raw_code wpb_raw_html').text.lower().strip()
                        remote = 'remote' if 'remote' in text else 'on-site'

                        self.get_jobs_dict(title, link, 'Bucuresti', remote)

        return self.jobs_list


exesoftware = ExeSoftware(
    company_name='exesoftware',
    url='https://www.exesoftware.ro/about/careers',
    logo_url='https://www.exesoftware.ro/wp-content/uploads/2022/02/logo-blue.png'
)
exesoftware.get_jobs()
#exesoftware.push_peviitor()
