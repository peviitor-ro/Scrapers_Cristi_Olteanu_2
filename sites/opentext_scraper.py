from src.scrapers import Scraper
from src.validate_city import validate_city


class OpenText(Scraper):

    def get_jobs(self):
        page = 0
        flag = True

        while flag:
            jobs = self.get_link_soup(self.url + str(page)).find_all('tr', class_='data-row')

            if len(jobs) > 0:

                for job in jobs:
                    link = 'https://careers.opentext.com' + job.find('a', class_='jobTitle-link')['href']
                    title = job.find('a', class_='jobTitle-link').text
                    city = job.find('span', class_='jobLocation').text.split(', ')[-2].strip()
                    country = job.find('span', class_='jobLocation').text.split(', ')[-1].split()[0]

                    if country != 'RO':
                        cities = self.get_link_soup(link).find_all('span', class_='jobGeoLocation')
                        for item in cities:
                            if 'RO' in item.text:
                                city = item.text.split(',')[0].strip('\n')

                    self.get_jobs_dict(title, link, validate_city(city))

            else:
                flag = False
            page += 25

        return self.jobs_list

open_text = OpenText(
    company_name='opentext',
    logo_url='https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/OpenText_logo.svg/447px-OpenText_logo.svg.png',
    url='https://careers.opentext.com/search/?q=&locationsearch=RO&startrow='

)
open_text.get_jobs()
open_text.push_peviitor()
