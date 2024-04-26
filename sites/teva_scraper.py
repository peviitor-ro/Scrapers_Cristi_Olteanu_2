from src.scrapers import Scraper


class Teva(Scraper):
    def __init__(self, company_name, url, logo_url):
        super().__init__(company_name, url, logo_url)

    def get_jobs(self):

        response = self.get_soup()
        jobs = response.find_all('tr', class_='data-row')

        for job in jobs:
            link = 'https://careers.teva' + job.find('a', class_='jobTitle-link')['href']
            title = job.find('a', class_='jobTitle-link').text
            city = job.find('span', class_='jobLocation').text.split(',')[0].strip()

            self.get_jobs_dict(title, link, self.get_validated_city(city))

        return self.jobs_list


teva = Teva(
    company_name='teva',
    url='https://careers.teva/search/?searchby=location&createNewAlert=false&q=&locationsearch=&geolocation=&optionsFacetsDD_facility=&optionsFacetsDD_department=Romania',
    logo_url='https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Teva_Pharmaceuticals_logo.png/800px-Teva_Pharmaceuticals_logo.png'
)
teva.get_jobs()
teva.push_peviitor()