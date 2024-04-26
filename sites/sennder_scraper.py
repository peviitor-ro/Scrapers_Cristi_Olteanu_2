from src.scrapers import Scraper


class Sennder(Scraper):
    def __init__(self, company_name, url, logo_url):
        super().__init__(company_name, url, logo_url)

    def get_jobs(self):
        response = self.get_soup()
        jobs = response.find_all('li', class_="mb-8")

        for job in jobs:
            title = job.find('div', class_="text-subsection-title mb-2 text-foreground-primary").text
            link = 'https://www.sennder.com/open-positions' + job.find('a')['href']
            city = self.get_validated_city(job.find('span', class_="text-foreground-secondary").text.split(',')[0])

            self.get_jobs_dict(title, link, city)

        return self.jobs_list


sennder = Sennder(
    company_name='sennder',
    url='https://www.sennder.com/open-positions/departments/all/locations/bucharest-romania',
    logo_url='https://uploads-ssl.webflow.com/5f0d9d156b2682a4ff0aaa3a/5f100c78742912bf9b8ef246_Logo%20Horizontal_Orange.svg'
)
sennder.get_jobs()
sennder.push_peviitor()
