from src.scrapers import Scraper


class Vevohub(Scraper):

    def get_jobs(self):

        jobs = self.get_soup().find_all('div', class_='elementor-flip-box')

        for job in jobs:
            title = job.find('h3', class_='elementor-flip-box__layer__title').text.strip()
            link = job.find('a', class_='elementor-flip-box__button elementor-button elementor-size-md')['href']
            self.get_jobs_dict(title, link, city='Bucuresti', county='Bucuresti')


vevohub = Vevohub(
    company_name='vevohub',
    url='https://vevohub.com/careers/',
    logo_url=''

)
vevohub.get_jobs()
vevohub.push_peviitor()
