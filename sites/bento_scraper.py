from src.scrapers import Scraper


class Bento(Scraper):

    def get_jobs(self):
        payload = {
            'filters': [],
            'logicalOperator': '',
            'sort': {
                'sortBy': '',
                'sortOrder': ''
            }
        }
        jobs = self.post_json(json=payload, params={'page': 1, 'pagesize': 25})['items']

        for job in jobs:
            title = job['jobTitle']
            link = 'https://bento.normahr.ro/careers-site/branch/c33e7207-eb18-4ac1-b01c-19276c41e562/jobs/' + job['pipelineID']

            self.get_jobs_dict(title, link, self.get_validated_city(job['location']))

        return self.jobs_list

bento = Bento(
    company_name='bento',
    url='https://be.normahr.ro/1n574nc3A/recruitment/api/v1/job-pipeline/careers/c33e7207-eb18-4ac1-b01c-19276c41e562',
    logo_url='https://www.bento.ro/wp-content/uploads/2022/03/Bento_logo.svg'
)
bento.get_jobs()
bento.push_peviitor()
