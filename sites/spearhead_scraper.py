from src.scrapers import Scraper


class Spearhead(Scraper):

    def get_jobs(self):
        response = self.get_soup()
        jobs = response.select(
            '#jobs_grid a[href*="/jobs/detail/"], #jobs_grid a.text-decoration-none'
        )

        for job in jobs:
            title_tag = job.find('h3')
            if title_tag is None:
                continue
            link = 'https://spearhead.systems' + job.get('href')
            title = title_tag.text.strip()

            self.get_jobs_dict(title, link, 'Bucuresti')

        return self.jobs_list


spearhead = Spearhead(
    company_name='spearhead',
    url='https://spearhead.systems/jobs',
    logo_url='https://www.romanianstartups.com/wp-content/uploads/2013/09/spearhead-systems-logo-177x100.jpg',
)
spearhead.get_jobs()
spearhead.push_peviitor()
