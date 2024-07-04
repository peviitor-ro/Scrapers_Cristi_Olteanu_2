from src.scrapers import Scraper


class ExeSoftware(Scraper):
    def __init__(self, company_name, url, logo_url):
        super().__init__(company_name, url, logo_url)

    def get_jobs(self):
        response = self.get_soup()
        jobs = response.find_all('div', class_='uncont')

        for job in jobs:
            info_link = job.find('a')

            if info_link:
                link = info_link.get('href') if 'jobs' in info_link.get('href') else None
                if link:
                    title = job.find('h5').text
                    try:
                        valid = self.get_link_soup(link).find('div', class_='uncode_text_column').find('h1')
                    except:
                        valid = None

                    if valid:

                        remote = 'remote' if ('remote' in job.find('span', class_='pill px-10 py-5 black mr-15 mb-15')
                                              .text.lower()) else 'on-site'

                        self.get_jobs_dict(title, link, 'Bucuresti', remote)

        return self.jobs_list


exesoftware = ExeSoftware(
    company_name= 'exesoftware',
    url='https://www.exesoftware.ro/about/careers',
    logo_url= 'https://www.exesoftware.ro/wp-content/uploads/2022/02/logo-blue.png'
)
exesoftware.get_jobs()
exesoftware.push_peviitor()
