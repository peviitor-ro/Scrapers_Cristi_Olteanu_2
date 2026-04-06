from src.scrapers import Scraper


class SuperBet(Scraper):

    def get_jobs(self):
        page = 1

        while True:
            response = self.get_link_soup(f'{self.url}&page={page}')
            jobs = response.find_all('a', href=True)
            found_jobs = False

            for job in jobs:
                link = job['href']

                if '/jobs/' not in link:
                    continue

                paragraphs = job.find_all('p')

                if len(paragraphs) < 2:
                    continue

                found_jobs = True
                title = paragraphs[0].text.strip()
                country = paragraphs[1].text.strip()

                if country == 'Romania':
                    self.get_jobs_dict(title, link, 'Bucuresti')

            if not found_jobs:
                break

            page += 1

        return self.jobs_list


superbet = SuperBet(
    company_name='superbet',
    url='https://job-boards.eu.greenhouse.io/superbet?offices%5B%5D=4005477101',
    logo_url='https://s101-recruiting.cdn.greenhouse.io/external_greenhouse_job_boards/logos/400/134/810/resized/favicon.png?1673612131'
)
superbet.get_jobs()
superbet.push_peviitor()
