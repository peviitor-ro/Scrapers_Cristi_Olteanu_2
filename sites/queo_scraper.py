from src.scrapers import Scraper


class Queo(Scraper):

    def get_jobs(self):

        response = self.get_json()['listItems']

        for job in response:
            if not all(job.get(key) for key in ('title', 'href', 'location')):
                continue

            title = job['title']
            link = f"https://www.queo.de{job['href']}"
            try:
                city = self.get_validated_city(job['location'])
            except:
                city = None

            if city is not None:
                self.get_jobs_dict(title, link, city)

        return self.jobs_list


queo = Queo(
    company_name='queo',
    url='https://www.queo.de/de/job/jobs.json',
    logo_url='https://asset.brandfetch.io/idUTj3lM0G/idE6RnDF2s.jpeg?updated=1709731691741'
)
queo.get_jobs()
queo.push_peviitor()
