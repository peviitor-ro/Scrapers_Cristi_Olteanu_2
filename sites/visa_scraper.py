from src.scrapers import Scraper


class Visa(Scraper):
    def __init__(self, company_name, url, logo_url):
        super().__init__(company_name, url, logo_url)

    def get_jobs(self):

        data = {"city": ["Bucharest"], "from": 0, "size": 10}
        response = self.post_json(headers=self.headers, json=data)['jobDetails']

        for job in response:
            title = job['jobTitle']
            link = 'https://corporate.visa.com/en/jobs/' + job['refNumber']

            self.get_jobs_dict(title, link, 'Bucuresti')

        return self.jobs_list


visa = Visa(
    company_name='visa',
    url='https://search.visa.com/CAREERS/careers/jobs?q=',
    logo_url='https://cdn.visa.com/v2/assets/images/logos/visa/blue/logo.png'
)
visa.get_jobs()
visa.push_peviitor()