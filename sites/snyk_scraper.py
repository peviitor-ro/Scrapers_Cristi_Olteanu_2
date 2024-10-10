from src.scrapers import Scraper


class Snyk(Scraper):

    def get_jobs(self):
        response = self.get_soup()
        jobs = response.find_all('div', class_='opening')

        for job in jobs:
            title = job.find('a').text
            link = 'https://boards.greenhouse.io/' + job.find('a')['href']
            locations = job.find('span', class_='location').text.split(',')
            cities = []

            for location in locations:
                if 'Cluj' in location or 'Bucharest' in location:
                    cities.append(self.get_validated_city(location.strip()))

            if cities:
                text_info = self.get_link_soup(link).find('div', {'id': 'content'}).text
                job_type = 'remote' if 'remote' in text_info else 'on-site'

                self.get_jobs_dict(title, link, cities, job_type)

        return self.jobs_list

snyk = Snyk(
    company_name='snyk',
    url='https://boards.greenhouse.io/snyk?gh_src=3f9b65652us',
    logo_url='https://snyk.io/_next/image/?url=https%3A%2F%2Fres.cloudinary.com%2Fsnyk%2Fimage%2Fupload%2Fv1669650003%2Fpress-kit%2Ftitle-card-logo-white-1.png&w=2560&q=75'
)
snyk.get_jobs()
snyk.push_peviitor()
