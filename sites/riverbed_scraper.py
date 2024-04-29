from src.scrapers import Scraper


class Riverbed(Scraper):
    def __init__(self, company_name, url, logo_url):
        super().__init__(company_name, url, logo_url)

    def get_jobs(self):
        querystring = {"ss": "1", "searchLocation": "13526", "in_iframe": "1"}
        response = self.get_soup(params=querystring)
        jobs = response.find_all('div', class_='row')

        for job in jobs:
            link_text = job.find('a')
            if link_text is not None:
                link = link_text['href']
                title = job.find('h3').text.strip()
                location_text = job.find('div', class_='col-xs-6 header left').text
                job_type = 'remote' if 'RO-Home Office' in location_text else 'hibrid'

                self.get_jobs_dict(title, link, 'Cluj-Napoca', job_type)

        return self.jobs_list


riverbed = Riverbed(
    url='https://emea-apj-riverbed.icims.com/jobs/search',
    company_name='riverbed',
    logo_url='https://cms.jibecdn.com/prod/riverbed/assets/HEADER-LOGO_IMG-en-us-1649182997894.png'

)
riverbed.get_jobs()
riverbed.push_peviitor()
