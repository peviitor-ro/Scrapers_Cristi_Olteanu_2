from src.scrapers import Scraper


class Queo(Scraper):
    def __init__(self, company_name, url, logo_url):
        super().__init__(company_name, url, logo_url)

    def get_jobs(self):

        response = self.get_json()['listItems']

        for job in response:
            title = job['title']
            link = f"https://www.queo.de/{job['href']}"
            try:
                city = self.get_validated_city(job['location'])
            except:
                city = None

            if city is not None:
                self.get_jobs_dict(title, link, city)

        return self.jobs_list


queo = Queo(
    company_name='queo',
    url='https://www.queo.de/en/job/jobs.json',
    logo_url='https://asset.brandfetch.io/idUTj3lM0G/idE6RnDF2s.jpeg?updated=1709731691741'
)
queo.get_jobs()
queo.push_peviitor()
