from src.scrapers import Scraper


class VaricentScraper(Scraper):

    def get_jobs(self):
        jobs = self.get_json(params={'content': 'true'})['jobs']

        for job in jobs:
            location = job.get('location', {}).get('name', '')

            if 'Romania' not in location:
                continue

            title = job['title'].strip()
            link = job['absolute_url']
            city = self.get_validated_city(location.split(',')[0].strip())
            metadata = job.get('metadata', [])
            job_type = 'on-site'

            for item in metadata:
                if item.get('name') == 'Employment Type' and 'remote' in item.get('value', '').lower():
                    job_type = 'remote'
                    break

            self.get_jobs_dict(title, link, city, job_type)

        return self.jobs_list


varicent = VaricentScraper(
    company_name='varicent',
    url='https://boards-api.greenhouse.io/v1/boards/varicent/jobs',
    logo_url='https://www.varicent.com/hubfs/favicon-transparent.png'
)
varicent.get_jobs()
varicent.push_peviitor()
