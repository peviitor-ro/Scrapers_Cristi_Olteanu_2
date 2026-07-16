import json
import re
from src.scrapers import Scraper
from src.validate_city import validate_city


class OpenText(Scraper):

    def get_jobs(self):
        from_page = 0
        page_size = 10

        while True:
            url = self.url if from_page == 0 else f'{self.url}&from={from_page}'
            soup = self.get_soup(url)

            jobs_data = self._extract_jobs_from_page(soup)
            if jobs_data is None:
                break

            jobs = jobs_data.get('data', {}).get('jobs', [])
            total_hits = jobs_data.get('totalHits', 0)

            for job in jobs:
                if job.get('country') != 'ROU':
                    continue

                title = job['title']
                job_id = job['jobId']
                slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
                link = f'https://careers.opentext.com/us/en/job/{job_id}/{slug}'
                city = validate_city(job.get('city', ''))

                self.get_jobs_dict(title, link, city)

            from_page += page_size
            if from_page >= total_hits:
                break

        return self.jobs_list

    @staticmethod
    def _extract_jobs_from_page(soup):
        for script in soup.find_all('script'):
            text = script.string or ''
            if 'eagerLoadRefineSearch' not in text:
                continue
            idx = text.find('"eagerLoadRefineSearch":')
            if idx < 0:
                continue
            start = text.find('{', idx)
            decoder = json.JSONDecoder()
            data, _ = decoder.raw_decode(text, start)
            return data
        return None


open_text = OpenText(
    company_name='opentext',
    logo_url='https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/OpenText_logo.svg/447px-OpenText_logo.svg.png',
    url='https://careers.opentext.com/us/en/search-results?p=ChIJw3aJlSb_sUARlLEEqJJP74Q&location=Romania'
)
open_text.get_jobs()
open_text.push_peviitor()
