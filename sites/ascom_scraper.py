from src.scrapers import Scraper


class Ascom(Scraper):

    def get_jobs(self):

        response = self.get_soup()
        jobs = response.find_all('li', class_='block-grid-item')

        for job in jobs:
            title_tag = job.find('span', class_='text-block-base-link')
            link_tag = job.find('a', href=True)

            if title_tag is None or link_tag is None:
                continue

            title = title_tag.get('title', title_tag.text.strip())
            link = link_tag['href']

            soup_job_type = self.get_link_soup(link)
            job_details = soup_job_type.find('dl', class_='company-links')
            job_type = 'on-site'

            if job_details is not None:
                labels = job_details.find_all('dt')
                values = job_details.find_all('dd')

                for label, value in zip(labels, values):
                    if label.text.strip() == 'Remote status':
                        job_type = value.text.strip().lower()
                        break

            self.get_jobs_dict(title, link, 'Cluj-Napoca', job_type)

        return self.jobs_list

ascom = Ascom(
    company_name='ascom',
    url='https://career.ascom.com/jobs?country=Romania&location=RO+Cluj-Napoca&query=',
    logo_url='https://upload.wikimedia.org/wikipedia/commons/thumb/e/ef/Logo_Ascom.svg/800px-Logo_Ascom.svg.png',
)
ascom.get_jobs()
ascom.push_peviitor()
