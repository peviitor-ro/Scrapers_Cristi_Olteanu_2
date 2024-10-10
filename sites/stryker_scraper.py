from src.scrapers import Scraper


class Stryker(Scraper):

    def get_jobs(self):
        payload = {
            "appliedFacets": {"Location_Country": ["f2e609fe92974a55a05fc1cdc2852122"]},
            "limit": 20,
            "offset": 0,
            "searchText": ""
        }
        response = self.post_json(json=payload)['jobPostings']

        for job in response:
            link = 'https://stryker.wd1.myworkdayjobs.com/en-US/StrykerCareers' + job['externalPath']
            title = job['title']
            link_job_info = 'https://stryker.wd1.myworkdayjobs.com/wday/cxs/stryker/StrykerCareers' + job['externalPath']
            city = job['locationsText'].split(',')[0]
            job_type = 'hybrid' if 'hybrid' in str(self.get_json_link(link_job_info)['jobPostingInfo']['jobDescription']).lower() else 'on-site'

            if 'locations' in city.lower():
                additional_locations = self.get_json_link(link_job_info)['jobPostingInfo']['additionalLocations']

                for additional_city in additional_locations:
                    if 'Bucharest' in additional_city:
                        city = 'Bucuresti'

            self.get_jobs_dict(title, link, self.get_validated_city(city), job_type)

        return self.jobs_list


stryker = Stryker(
    company_name='Stryker',
    url='https://stryker.wd1.myworkdayjobs.com/wday/cxs/stryker/StrykerCareers/jobs',
    logo_url='https://stryker.wd1.myworkdayjobs.com/wday/cxs/stryker/StrykerCareers/sidebarimage/7bed2480eb810113b6d12edd2602fe00'
)
stryker.get_jobs()
stryker.push_peviitor()
