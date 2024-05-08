from src.scrapers import Scraper
import json


class Blankfactor(Scraper):
    def __init__(self, company_name, url, logo_url):
        super().__init__(company_name, url, logo_url)

    def get_jobs(self):
        payload = {
            "appliedFacets": {"locations": ["893948fa336d1000cd34c9b0904c0000", "893948fa336d1000cd5db9fd84360000"]},
            "limit": 20,
            "offset": 0,
            "searchText": ""
        }
        headers = self.get_cookies('wd-browser-id', 'PLAY_SESSION', ' vps-cke', 'WorkdayLB_UI_Apache')

        response = self.post_json(headers=headers, json=payload)['jobPostings']

        for job in response:
            title = job['title']
            link = f"https://blankfactor.wd12.myworkdayjobs.com/en-US/Blankfactor_External{job['externalPath']}"
            link_info = f"https://blankfactor.wd12.myworkdayjobs.com/wday/cxs/blankfactor/Blankfactor_External{job['externalPath']}"
            first_city = self.get_validated_city(job['locationsText'].split()[-1])
            romanian_cities = ['Cluj-Napoca', 'Bucuresti']
            first_city_link = self.get_validated_city(self.get_json_link(link_info)['jobPostingInfo']['location'].split()[-1])

            cities = [first_city] if first_city in romanian_cities else []

            try:
                additional_locations = [
                    self.get_validated_city(city.split()[-1])
                    for city in self.get_json_link(link_info)['jobPostingInfo']['additionalLocations']]
            except KeyError:
                additional_locations = []

            cities.extend([loc for loc in additional_locations if loc in romanian_cities])

            if first_city_link in romanian_cities and first_city != first_city_link:
                cities.append(first_city_link)

            self.get_jobs_dict(title, link, cities)

        return self.jobs_list


blankfactor = Blankfactor(
    company_name='blankfactor',
    url='https://blankfactor.wd12.myworkdayjobs.com/wday/cxs/blankfactor/Blankfactor_External/jobs',
    logo_url='https://thepaymentsassociation.org/wp-content/uploads/sites/7/2023/07/Untitled-design-2023-07-24T151941.073.png'
)
blankfactor.get_jobs()
blankfactor.push_peviitor()
