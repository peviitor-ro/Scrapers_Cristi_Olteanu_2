from src.scrapers import Scraper


class Sennder(Scraper):

    def get_jobs(self):
        payload = {
            'operationName': 'JobBoardList',
            'variables': {'boardId': 'senndertechnologies-gmbh'},
            'query': 'query JobBoardList($boardId: String!) { oatsExternalJobPostings(boardId: $boardId) { jobPostings { extId title locations { city isoCountry isRemote } } } }'
        }
        jobs = self.post_json(
            headers={'User-Agent': self.headers['User-Agent']},
            json=payload
        )['data']['oatsExternalJobPostings']['jobPostings']

        for job in jobs:
            locations = job.get('locations') or []

            for location in locations:
                if location.get('isoCountry') != 'ROU':
                    continue

                city = self.get_validated_city(location['city'])
                link = f"https://jobs.gem.com/senndertechnologies-gmbh/{job['extId']}"
                remote = 'remote' if location.get('isRemote') else 'on-site'

                self.get_jobs_dict(job['title'].strip(), link, city, remote)

        return self.jobs_list


sennder = Sennder(
    company_name='sennder',
    url='https://jobs.gem.com/api/public/graphql',
    logo_url='https://a.storyblok.com/f/341309/ce59cf62f1/logo.svg'
)
sennder.get_jobs()
sennder.push_peviitor()
