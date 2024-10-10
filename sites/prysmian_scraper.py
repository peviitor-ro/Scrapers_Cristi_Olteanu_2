from src.scrapers import Scraper


class Prysmian(Scraper):

    def get_response(self, offset):
        headers = self.get_cookies('wd-browser-id', 'PLAY_SESSION', '__cf_bm', '__cflb', '_cfuvid')
        response = self.post_json(headers=headers, json={
            "appliedFacets": {"locationCountry": ["f2e609fe92974a55a05fc1cdc2852122"]},
            "limit": 20,
            "offset": offset,
        })
        return response

    def get_jobs(self):

        number_jobs = self.get_response(0)['total']

        for i in range(0, number_jobs, 20):
            jobs = self.get_response(i)['jobPostings']

            for job in jobs:
                title = job['title']
                link = 'https://prysmiangroup.wd3.myworkdayjobs.com/en-US/Careers' + job['externalPath']
                base_job_type = job.get('remoteType')
                job_type = 'hybrid' if base_job_type is not None and 'hybrid' in base_job_type.lower() else 'on-site'

                self.get_jobs_dict(title, link, 'Slatina', job_type, 'Olt')

        return self.jobs_list


prysmian = Prysmian(
    company_name='prysmian',
    url='https://prysmiangroup.wd3.myworkdayjobs.com/wday/cxs/prysmiangroup/Careers/jobs',
    logo_url=''
)
prysmian.get_jobs()
prysmian.push_peviitor()

