from src.scrapers import Scraper


class Mindspace(Scraper):

    def get_jobs(self):
        jobs = self.get_soup().find_all('div', class_='afb-careers-lobby__job')

        for job in jobs:
            title = job.find('div', class_='afb-careers-lobby__job-name').text.strip()
            link = job.find('a', class_='afb-careers-lobby__job-link').get('href')
            city_el = job.find('div', class_='afb-careers-lobby__job-city')

            if city_el is None:
                continue

            city = city_el.text.strip()

            self.get_jobs_dict(title, link, city)

        return self.jobs_list


mindpspace = Mindspace(
    company_name='Mindspace',
    url='https://www.mindspace.me/careers/',
    logo_url=''
)
mindpspace.get_jobs()
mindpspace.push_peviitor()
