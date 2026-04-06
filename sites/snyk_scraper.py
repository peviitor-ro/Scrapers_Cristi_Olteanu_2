from src.scrapers import Scraper


class Snyk(Scraper):

    def get_jobs(self):
        jobs = self.get_json().get('data', [])

        for job in jobs:
            title = job['title'].strip()
            link = job['url']
            locations = job.get('locations', [])
            locations = locations if isinstance(locations, list) else [locations]

            for location in locations:
                location_name = location.get('@_Descriptor', '')

                if 'Romania' not in location_name:
                    continue

                city = location_name.split(' - ', 1)[-1].replace(' Office', '').replace(' Local', '').strip()
                city = self.get_validated_city(city)
                job_type = 'remote' if 'remote' in location_name.lower() else 'on-site'

                self.get_jobs_dict(title, link, city, job_type)

        return self.jobs_list


snyk = Snyk(
    company_name='snyk',
    url='https://snyk.io/api/next/jobs/',
    logo_url='https://snyk.io/_next/image/?url=https%3A%2F%2Fres.cloudinary.com%2Fsnyk%2Fimage%2Fupload%2Fv1669650003%2Fpress-kit%2Ftitle-card-logo-white-1.png&w=2560&q=75'
)
snyk.get_jobs()
snyk.push_peviitor()
