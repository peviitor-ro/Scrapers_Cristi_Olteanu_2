from src.scrapers import Scraper


class Wyser(Scraper):
    def __init__(self, company_name, url, logo_url):
        super().__init__(company_name, url, logo_url)

    def get_jobs(self):

        response = self.get_soup()
        jobs = response.find_all('article', class_='px-0 col-12 col-sm-6 col-xl-4 py-3 card-job')

        for job in jobs:
            link = job.find('a', class_='dettaglio')['href']
            title = job.find('div', class_='col-10').text.strip()
            city = job.find('li', class_='card-text size-16 blue font-weight-bold posto').text.split(',')[0]

            self.get_jobs_dict(title, link, city)

        return self.jobs_list


wyser = Wyser(
    company_name='Wyser',
    url='https://ro.wyser-search.com/job-offers/',
    logo_url='https://ro.mywyser.com/assets/images/logo-wyser.png'
)
wyser.get_jobs()
wyser.push_peviitor()
