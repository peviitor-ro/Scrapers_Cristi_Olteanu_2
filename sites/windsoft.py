from src.scrapers import Scraper


class Windsoft(Scraper):

    def get_jobs(self):

        jobs = self.get_soup().find_all('div', class_='col-xs-12 col-sm-6 col-md-4 col-lg-4 mv-20')

        for job in jobs:
            title = job.find('div', class_='career_name blue').text
            link = 'https://www.windsoft.ro' + job.find('a').get('href')
            city = job.find('div', class_='career_location').text.title()

            self.get_jobs_dict(title, link, city)


windsoft = Windsoft(
    company_name='Windsoft',
    url='https://www.windsoft.ro/ro/cariere',
    logo_url=''
)
windsoft.get_jobs()
windsoft.push_peviitor()
