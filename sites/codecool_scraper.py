import re

import requests

from src.scrapers import Scraper


class CodeCool(Scraper):

    careers_page_url = 'https://codecool.com/careers/'
    job_link_base = 'https://codecool.bamboohr.com/careers/'

    def get_jobs(self):

        jobs = self.get_bamboohr_jobs()

        if not jobs:
            jobs = self.get_careers_page_jobs()

        for job in jobs:
            link = self.job_link_base + job['id']

            self.get_jobs_dict(job['title'], link, 'Bucuresti', job['remote'])

    def get_bamboohr_jobs(self):

        try:
            response = self.get_json()
        except (requests.exceptions.RequestException, ValueError):
            return []

        if not isinstance(response, dict):
            return []

        jobs = []

        for job in response.get('result') or []:
            job_id = job.get('id')
            title = job.get('jobOpeningName')

            if not job_id or not title:
                continue

            jobs.append({
                'id': job_id,
                'title': title,
                'remote': 'remote' if job.get('locationType') == '1' else 'on-site'
            })

        return jobs

    def get_careers_page_jobs(self):

        soup = self.get_link_soup(self.careers_page_url)

        jobs = []

        for item in soup.find_all('div', class_='jet-listing-grid__item'):
            anchor = item.find('a', href=re.compile(r'codecool\.bamboohr\.com/careers/'))

            if not anchor:
                continue

            fields = [field.get_text(strip=True) for field in item.select('.jet-listing-dynamic-field__content')]

            if not fields:
                continue

            job_id = anchor['href'].split('/careers/')[-1].split('?')[0].strip('/')

            jobs.append({
                'id': job_id,
                'title': fields[0],
                'remote': 'on-site'
            })

        return jobs


codecool = CodeCool(
    company_name='codecool',
    url='https://codecool.bamboohr.com/careers/list',
    logo_url=''
)
codecool.get_jobs()
codecool.push_peviitor()

