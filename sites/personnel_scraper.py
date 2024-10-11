from src.scrapers import Scraper
from src.validate_city import validate_city


class Personnel(Scraper):

    def get_jobs(self):
        page = 1
        flag = True

        while flag:

            response = self.get_link_soup(f'https://personnel.com.ro/posturi-disponibile/?page={page}%2F')
            jobs = response.find_all('div', class_='list-data')

            if len(jobs) > 0:

                for job in jobs:
                    link = job.find('a')['href']
                    title = job.find('span', class_='job-title').text
                    city = job.find('div', class_='job-location').text.split(',')
                    city = [validate_city(c.strip()) for c in city if c.strip() != 'Ilfov']

                    self.get_jobs_dict(title, link, city)
                page += 1
            else:
                flag = False

        return self.jobs_list


personnel = Personnel(
    company_name='Personnel',
    url='https://personnel.com.ro/posturi-disponibile/?page=4%2F',
    logo_url='https://personnel.com.ro/wp-content/uploads/2018/08/personnel_logo-site.png'
)
personnel.get_jobs()
personnel.push_peviitor()


