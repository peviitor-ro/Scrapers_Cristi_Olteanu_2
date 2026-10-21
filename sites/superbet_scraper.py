from src.scrapers import Scraper


class SuperBet(Scraper):

    def get_jobs(self):
        page = 1

        while True:
            response = self.get_link_soup(f'{self.url}?page={page}')
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
    url='https://job-boards.eu.greenhouse.io/super',
    logo_url='https://s101-recruiting.cdn.greenhouse.io/external_greenhouse_job_boards/logos/400/134/810/original/Super-Logo.jpg?1765813793'
)
superbet.get_jobs()
superbet.push_peviitor()
