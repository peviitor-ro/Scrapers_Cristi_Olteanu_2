from src.scrapers import Scraper

class Operative(Scraper):
    def __init__(self, company_name, url, logo_url):
        super().__init__(company_name, url, logo_url)

    def get_jobs(self):
        jobs = self.get_json()['result']
        for job in jobs:
            title = job['jobOpeningName']
            link = f"https://operative.bamboohr.com/careers/{job['id']}?source=aWQ9NA=="
            print(link)




operative = Operative(
    company_name= 'Operative',
    logo_url='https://images4.bamboohr.com/141701/logos/cropped.jpg?v=38',
    url= 'https://operative.bamboohr.com/careers/list'
)
operative.get_jobs()