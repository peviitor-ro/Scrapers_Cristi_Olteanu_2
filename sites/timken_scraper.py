from src.scrapers import Scraper


class Timken(Scraper):

    def get_jobs(self):

        response = self.get_soup()
        jobs = response.find_all('tr', class_='data-row')

        for job in jobs:
            title = job.find('a', class_='jobTitle-link').text
            link = 'https://careers.timken.com/job.find' + job.find('a', class_='jobTitle-link')['href']
            country = job.find('span', class_='jobLocation').text.split(', ')[-2]
            city = job.find('span', class_='jobLocation').text.split()[0].strip(',')

            if 'RO' in country:
                self.get_jobs_dict(title, link, city)

        return self.jobs_list


timken = Timken(
    company_name='timken',
    url='https://careers.timken.com/search/?q=&q2=&alertId=&locationsearch=&title=&location=Ro&department=',
    logo_url='https://getvectorlogo.com/wp-content/uploads/2019/05/the-timken-company-vector-logo.png'
)
timken.get_jobs()
timken.push_peviitor()
