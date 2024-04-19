from src.scrapers import Scraper


class MunchScraper(Scraper):

    def __init__(self, company_name, url, logo_url):
        super().__init__(company_name, url, logo_url)

    def get_jobs(self):

        response = self.get_soup(params={"split_view":"false","geobound_coordinates[top_left_lat]":"44.427807765515226","geobound_coordinates[top_left_lon]":"26.098462343215942","geobound_coordinates[bottom_right_lat]":"44.425723714377156","geobound_coordinates[bottom_right_lon]":"26.106610894203186","query":""})
        jobs = response.find_all('li', class_='w-full')

        for job in jobs:
            title = job.find('span', class_='text-block-base-link sm:min-w-[25%] sm:truncate company-link-style'
                           )['title']

            link = job.find('a', class_='flex flex-col py-6 text-center sm:px-6 hover:bg-gradient-block-base-bg focus-visible-company focus-visible:rounded'
                            )['href']

            info_job = job.find('div', class_='mt-1 text-md').text

            if 'Bucharest' in info_job:
                city = 'Bucuresti'
            else:
                city = ''

            if 'Hybrid' in info_job:
                job_type = 'hibrid'
            elif 'Remote' in info_job and 'Hybrid' not in info_job:
                job_type = 'Remote'
            else:
                job_type = 'On-site'

            self.get_jobs_dict(title, link, city, job_type)

        return self.jobs_list


munch = MunchScraper(
    company_name='munch',
    url='https://careers.munch.eco/jobs',
    logo_url='https://images.teamtailor-cdn.com/images/s3/teamtailor-production/logotype-v3/image_uploads/545c8b01-f937-4b14-9bcd-abf5d2a8f7ef/original.png'
)

munch.get_jobs()
munch.push_peviitor()
