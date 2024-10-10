from src.scrapers import Scraper


class Neovision(Scraper):

    def get_jobs(self):

        response = self.get_soup()
        jobs = response.find_all('div', class_='careers-openings-item')

        for job in jobs:
            link = job.find('a')['href']
            title = job.find('span', class_='button-casestudy-text text-h2').text

            self.get_jobs_dict(title, link, 'Bucuresti')

        return self.jobs_list


neovision = Neovision(
    company_name='neovision',
    url='https://neovision.dev/careers/',
    logo_url='https://www.highcontrast.ro/wp-content/uploads/2020/12/Neo-Vision-2.png'
)
neovision.get_jobs()
neovision.push_peviitor()
