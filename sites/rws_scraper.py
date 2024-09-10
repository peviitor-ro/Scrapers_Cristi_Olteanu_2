from src.scrapers import Scraper


class Rws(Scraper):
    def __init__(self, company_name, url, logo_url):
        super().__init__(company_name, url, logo_url)

    def get_jobs(self):
        querystring = {"ss": "1", "in_iframe": "1", "searchLocation": "13526--"}
        response = self.get_soup(params=querystring)
        jobs = response.find_all('div', class_='row')

        for job in jobs:
            text = job.find('a', class_='iCIMS_Anchor')

            if text is not None:
                part_title = text['title'].split("-")
                title = str(''.join(part_title[1:])).strip()
                link = text['href']
                job_type = 'remote' if 'remote' in self.get_link_soup(link).find('div', class_='col-xs-6 header left').text.strip().lower() else 'on-site'

                self.get_jobs_dict(title, link, 'Cluj-Napoca', job_type)

        return self.jobs_list


rws = Rws(
    company_name='rws',
    url='https://globalcareers-rws.icims.com/jobs/search#iCIMS_Header',
    logo_url='https://c-13850-20230914-www-rws-com.i.icims.com/media/images/Artboard-1_tcm228-187294.svg?v=NjM4MjcwODY1NTA3MTQyMTkw',
)
rws.get_jobs()
rws.push_peviitor()
