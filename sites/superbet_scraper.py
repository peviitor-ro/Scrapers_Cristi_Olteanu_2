from src.scrapers import Scraper


class SuperBet(Scraper):

    def get_jobs(self):
        response = self.get_soup()
        jobs = response.find_all('div', class_='opening')

        for job in jobs:
            link = 'https://boards.eu.greenhouse.io/' + job.find('a')['href']
            title = job.find('a').text
            country = job.find('span', class_='location').text

            if 'Romania' in country:
                self.get_jobs_dict(title, link, 'Bucuresti')

        return self.jobs_list


superbet = SuperBet(
    company_name='superbet',
    url='https://boards.eu.greenhouse.io/superbet',
    logo_url='https://s101-recruiting.cdn.greenhouse.io/external_greenhouse_job_boards/logos/400/134/810/resized/favicon.png?1673612131'
)
superbet.get_jobs()
superbet.push_peviitor()
