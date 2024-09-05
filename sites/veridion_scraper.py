from src.scrapers import Scraper


class Veridion(Scraper):
    def __init__(self, company_name, url, logo_url):
        super().__init__(company_name, url, logo_url)

    def get_jobs(self):
        response = self.get_soup()
        jobs = response.find_all('div', class_='career-wrap')

        for job in jobs:
            title = job.find('h2', class_='fw-bold').text.strip()
            link = job.find('a', class_='d-inline-block w-100 careers-apply transition-ltr-white-black text-decoration-none')['href']
            location_info = job.find('h5', class_='light-grey').text.strip()
            city = 'Bucuresti' if 'Bucharest' in location_info else ''
            job_type = 'hybrid' if 'hybrid' in location_info else 'on-site'

            self.get_jobs_dict(title, link, city, job_type)

        return self.jobs_list

veridion = Veridion(
    company_name='veridion',
    url='https://veridion.com/careers/',
    logo_url='https://veridion.com/wp-content/themes/soleadify/assets/images/graphical-elements/main-logo.png'
)
veridion.get_jobs()
veridion.push_peviitor()
