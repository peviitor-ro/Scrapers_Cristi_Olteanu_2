from src.scrapers import Scraper


class GlobalStep(Scraper):

    def get_jobs(self):
        response = self.post_html(data='jq=&awsm_job_spec%5Bjob-category%5D=&awsm_job_spec%5Bjob-location%5D=77&lang=en&action=jobfilter&listings_per_page=20',
                                  headers={
                                      "Content-Type": "application/x-www-form-urlencoded",
                                      "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
                                  })
        jobs = response.find_all('div', class_='awsm-job-listing-item awsm-grid-item')

        for job in jobs:
            link = job.find('a', class_='awsm-job-item')['href']
            title = job.find('h2', class_='awsm-job-post-title').text.strip()
            text = job.find('span', class_='awsm-job-specification-term').text
            city = self.get_validated_city(text.split()[-1])
            job_type = 'remote' if 'remote' in text.lower() else 'on-site'

            self.get_jobs_dict(title, link, city, job_type)

        return self.jobs_list


globalstep = GlobalStep(
    company_name='globalstep',
    url='https://globalstep.com/wp-admin/admin-ajax.php',
    logo_url='https://mma.prnewswire.com/media/1394631/GlobalStep_Logo.jpg?w=200'
)
globalstep.get_jobs()
globalstep.push_peviitor()


