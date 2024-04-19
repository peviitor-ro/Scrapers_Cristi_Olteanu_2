from sites.src.scrapers import Scraper


class Xylem(Scraper):
    def __init__(self, company_name, url, logo_url):
        super().__init__(company_name, url, logo_url)

    def get_jobs(self):

        response = self.get_soup()
        jobs = response.find_all('tr')

        for job in jobs:
            title = job.find('a').text
            link = 'https://jobs.jobvite.com/' + job.find('a')['href']
            city = job.find('td', class_='jv-job-list-location').text.split(',')[0].strip()

            if validated_city := self.get_validated_city(city):
                self.get_jobs_dict(title, link, validated_city)

        return self.jobs_list

xylem = Xylem(
    company_name='xylem',
    url='https://jobs.jobvite.com/xylem/search?r=&l=Bucharest,%20Romania&c=&q=',
    logo_url='https://www.xylem.com/siteassets/brand/_logos/color-lockups-transparent/xylem_tag_7704c.svg'
)

xylem.get_jobs()
xylem.push_peviitor()
