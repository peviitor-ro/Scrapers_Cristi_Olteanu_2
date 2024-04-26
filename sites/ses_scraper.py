from src.scrapers import Scraper


class Ses(Scraper):
    def __init__(self, company_name, url, logo_url):
        super().__init__(company_name, url, logo_url)

    def get_jobs(self):
        response = self.get_soup()
        jobs = response.find_all('tr', class_='data-row')

        for job in jobs:
            link = 'https://careers.ses.com' + job.find('a', class_='jobTitle-link')['href']
            title = job.find('a', class_='jobTitle-link').text
            city = self.get_validated_city(job.find('span', class_='jobLocation').text.split(',')[0].strip())

            self.get_jobs_dict(title, link, city)

        return self.jobs_list


ses = Ses(
    company_name='ses',
    url='https://careers.ses.com/search/?createNewAlert=false&q=&locationsearch=Romania&optionsFacetsDD_customfield3=&optionsFacetsDD_customfield5=',
    logo_url='https://upload.wikimedia.org/wikipedia/commons/thumb/9/9d/SES_Logo_claim_BL_M_png.png/1600px-SES_Logo_claim_BL_M_png.png?20151208115653'
)
ses.get_jobs()
ses.push_peviitor()