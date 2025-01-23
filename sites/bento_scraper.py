from src.scrapers import Scraper


class Bento(Scraper):

    def get_jobs(self):
        response = self.get_soup()
        jobs = response.find_all('div', class_='tm-box-icon style-01 tm-animation move-up')

        for job in jobs:
            title = job.find('h4', class_='heading').text.strip()
            link = job.find('a')['href']

            self.get_jobs_dict(title, link, 'Bucuresti')

        return self.jobs_list

bento = Bento(
    company_name='bento',
    url='https://www.bento.ro/cariere/',
    logo_url='https://www.bento.ro/wp-content/uploads/2022/03/Bento_logo.svg'
)
bento.get_jobs()
bento.push_peviitor()
