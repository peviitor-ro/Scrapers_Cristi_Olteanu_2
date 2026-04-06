import re

from src.scrapers import Scraper


class TeConnectivity(Scraper):

    def get_jobs(self):
        page = self.get_link_soup('https://careers.te.com/search/?createNewAlert=false&q=&locationsearch=Romania&optionsFacetsDD_customfield3=&optionsFacetsDD_department=')
        csrf_token = re.search(r'var CSRFToken = "([^"]+)";', str(page))

        if csrf_token is None:
            return self.jobs_list

        payload = {
            'keywords': '',
            'locale': 'en_US',
            'location': 'Romania',
            'pageNumber': 0,
            'sortBy': 'recent'
        }
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': self.headers['User-Agent'],
            'X-CSRF-Token': csrf_token.group(1)
        }
        jobs = self.post_json(headers=headers, json=payload)['jobSearchResult']

        for job in jobs:
            response = job['response']
            title = response['unifiedStandardTitle'].strip()
            city = self.get_validated_city(response['jobLocationShort'][0].split(',')[0].strip().title())
            link = f"https://careers.te.com/job/{response['unifiedUrlTitle']}/{response['id']}-en_US"
            job_type = 'remote' if 'remote' in title.lower() else 'on-site'

            self.get_jobs_dict(title, link, city, job_type)

        return self.jobs_list


teconnectivity = TeConnectivity(
    company_name='TeConnectivity',
    url='https://careers.te.com/services/recruiting/v1/jobs',
    logo_url='https://rmkcdn.successfactors.com/e2907dff/905ce309-95ed-4020-875d-3.jpg'
)
teconnectivity.get_jobs()
teconnectivity.push_peviitor()
