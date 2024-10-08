from src.scrapers import Scraper
import re


class Personnel(Scraper):

    def get_jobs(self):
        response = self.get_soup()
        jobs = response.find_all('div', class_='list-data')

        for job in jobs:
            link = job.find('a')['href']
            title = job.find('span', class_='job-title').text
            city = re.split(r"(?<=,) \s+|/", job.find('div', class_='job-location').text)

            self.get_jobs_dict(title, link, city)

        return self.jobs_list


personnel = Personnel(
    company_name='Personnel',
    url='https://personnel.com.ro/posturi-disponibile/',
    logo_url='https://personnel.com.ro/wp-content/uploads/2018/08/personnel_logo-site.png'
)
personnel.get_jobs()
personnel.push_peviitor()


