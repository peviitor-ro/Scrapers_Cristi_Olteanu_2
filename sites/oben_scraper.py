from src.scrapers import Scraper


class Oben(Scraper):

    def get_jobs(self):

        querystring = {"page_size": "50", "page": "1", "city_new__in": "", "organization__in": "",
                       "ordering": "-is_pinned_in_career_page,-last_published_at"}
        jobs = self.get_json(params=querystring)['results']

        for job in jobs:
            title = job['position_name']
            link = 'https://www.careers-page.com/oben-technology/job/' + job['hash']
            city = self.get_validated_city(job['city'])
            self.get_jobs_dict(title, link, city)

        return self.jobs_list

oben = Oben(
    company_name='ObenTechnology',
    url='https://www.careers-page.com/api/v1.0/c/oben-technology/jobs/',
    logo_url='https://manatal-backend-public-assets.s3.amazonaws.com/media/career_portal_logo_direct_upload/b81ef1de-4098-4e0a-af8c-b3c5858e412f_oben-logo-268x268.png'
)
oben.get_jobs()
oben.push_peviitor()

