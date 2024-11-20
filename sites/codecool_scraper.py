from src.scrapers import Scraper


class CodeCool(Scraper):

    def get_jobs(self):

        jobs = self.get_json()['result']

        for job in jobs:
            remote = 'remote' if job['locationType'] == '1' else 'on-site'
            if remote == 'remote':
                title = job['jobOpeningName']
                link = 'https://codecool.bamboohr.com/careers/' + job['id']

                self.get_jobs_dict(title, link, 'Bucuresti', remote)


codecool = CodeCool(
    company_name='codecool',
    url='https://codecool.bamboohr.com/careers/list',
    logo_url=''
)
codecool.get_jobs()
codecool.push_peviitor()

