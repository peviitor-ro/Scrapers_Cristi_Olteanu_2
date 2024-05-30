from src.scrapers import Scraper


class Nix(Scraper):
    def __init__(self, company_name, url, logo_url):
        super().__init__(company_name, url, logo_url)

    def get_jobs(self):

        page = 1
        flag = True

        while flag:
            response = self.get_link_soup(f'https://careers.n-ix.com/jobs/page/{page}/?country%5B0%5D=Romania&keyword')
            jobs = response.find_all('div', class_='job-card-sm')

            if len(jobs) > 0:
                for job in jobs:
                    title = job.find('a', class_='title').text
                    link = job.find('a', class_='title')['href']
                    info = job.find('div', class_='info-list').text.lower()
                    job_type = []
                    if 'office' in info:
                        job_type.append('on-site')
                    if 'remote' in info:
                        job_type.append('remote')

                    self.get_jobs_dict(title, link, 'Bucuresti', job_type)
            else:
                flag = False
            page += 1

        return self.jobs_list


nix = Nix(
    company_name='N-iX',
    url='https://careers.n-ix.com/jobs/?country%5B%5D=Romania&keyword=',
    logo_url='https://careers.n-ix.com/wp-content/themes/careers/assets/theme/img/website_logo.png'
)
nix.get_jobs()
nix.push_peviitor()