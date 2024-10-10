from src.scrapers import Scraper


class Temps(Scraper):

    def get_jobs(self):
        response = self.get_soup()
        jobs = response.find_all('li', class_='media')

        for job in jobs:
            link_text = job.find('a', class_='text-secondary').get('href')

            if link_text is not None:
                link = 'https://www.careers-page.com' + link_text
                title = str(job.find('h5')).split('\n')[1].strip()
                city = self.get_validated_city(str(job.find('span', attrs={'style': 'margin-right: 10px;'})
                                                   ).split('i>')[1].split(',')[0].strip())
                self.get_jobs_dict(title, link, city)

        return self.jobs_list

temps = Temps(
    company_name='temps',
    url='https://www.careers-page.com/temps-hr-2',
    logo_url='https://manatal-backend-public-assets.s3.amazonaws.com/media/career_portal_logo_direct_upload/e74c9c7b-01ee-4899-a1b9-684ba18c7a0e_Temps%20-%20logo%20-%20final.png'
)
temps.get_jobs()
temps.push_peviitor()
