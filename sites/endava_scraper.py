from src.scrapers import Scraper


class Endava(Scraper):

    def get_jobs_per_city(self, city, page):
        headers = self.get_cookies('AWSALB', 'AWSALBCORS')
        querystring = {"search": "Romania", "type": "location", "value": f"{city}, RO", "page": f"{page}"}
        jobs = self.get_soup(params=querystring, headers=headers).select('a.link--block.details')

        if jobs:
            for job in jobs:
                title = job.select_one('h4.details-title.job-title.link--block-target').text
                link_job = job.get('href')

                self.get_jobs_dict(title, link_job, self.get_validated_city(city))
            return self.jobs_list
        else:
            return None

    def get_jobs(self):

        headers = self.get_cookies('AWSALB', 'AWSALBCORS')
        link = 'https://careers.smartrecruiters.com/Endava'
        querystring = {"search": "Romania"}
        city_slots = self.get_link_soup(link=link, params=querystring, headers=headers).select('ul.list--dotted.title-list')

        city_hash = {slot.select_one('h3.opening-title.title.display--inline-block.text--default').text.split(',')[0]:
                         int(slot.select_one('span.title').text.split()[0])
                     for slot in city_slots}

        for key, value in city_hash.items():
            page = 0
            if value < 9:
                self.get_jobs_per_city(key, page)
            else:
                flag = True
                while flag:
                    if self.get_jobs_per_city(key, page) is not None:
                        page += 1
                    else:
                        flag = False


endava = Endava(
    company_name='endava',
    url='https://careers.smartrecruiters.com/Endava/api/more',
    logo_url=''
)
endava.get_jobs()
endava.push_peviitor()
