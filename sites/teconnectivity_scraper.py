from src.scrapers import Scraper


class TeConnectivity(Scraper):

    def get_jobs(self):

        response = self.get_soup()
        jobs = response.find_all('tr', class_='data-row')

        for job in jobs:
            link = 'https://careers.te.com' + job.find('a', class_='jobTitle-link')['href']
            title = job.find('a', class_='jobTitle-link').text
            city = str(job.find('span', class_='jobLocation').text.split(',')[0].strip()).capitalize()
            job_type = 'remote' if 'remote' in title.lower() else 'on-site'

            self.get_jobs_dict(title, link, city, job_type)

        return self.jobs_list


teconnectivity = TeConnectivity(
    company_name='TeConnectivity',
    url='https://careers.te.com/search/?createNewAlert=false&q=&locationsearch=Romania&optionsFacetsDD_customfield3=&optionsFacetsDD_department=',
    logo_url='https://rmkcdn.successfactors.com/e2907dff/905ce309-95ed-4020-875d-3.jpg'
)
teconnectivity.get_jobs()
teconnectivity.push_peviitor()
