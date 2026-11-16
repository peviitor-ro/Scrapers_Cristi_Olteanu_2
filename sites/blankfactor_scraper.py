from src.scrapers import Scraper


class Blankfactor(Scraper):

    def get_jobs(self):
        payload = {
            "appliedFacets": {"locations": ["6be8deca68431009366e3572eea60000", "893948fa336d1000cd5db9fd84360000", "893948fa336d1000cd34c9b0904c0000"]},
            "limit": 20,
            "offset": 0,
            "searchText": ""
        }
        headers = self.get_cookies('wd-browser-id', 'PLAY_SESSION', 'wday_vps_cookie', 'vps-cke', '__cf_bm', '__cflb', '_cfuvid')
        if not headers:
            headers = self.headers.copy()
            headers['Content-Type'] = 'application/json'
            headers['Accept'] = 'application/json'

        try:
            response = self.post_json(headers=headers, json=payload)
        except Exception:
            return self.jobs_list

        if not isinstance(response, dict) or 'jobPostings' not in response:
            return self.jobs_list
        jobs = response['jobPostings'] or []

        romanian_cities = ['Cluj-Napoca', 'Bucuresti']
        for job in jobs:
            try:
                job_type = 'on-site'
                title = job['title']
                link = f"https://blankfactor.wd12.myworkdayjobs.com/en-US/Blankfactor_External{job['externalPath']}"
                link_info = f"https://blankfactor.wd12.myworkdayjobs.com/wday/cxs/blankfactor/Blankfactor_External{job['externalPath']}"

                locations_text = (job.get('locationsText') or '').strip()
                first_city = self.get_validated_city(locations_text.split()[-1]) if locations_text else None

                try:
                    job_info = self.get_json_link(link_info).get('jobPostingInfo', {})
                except Exception:
                    job_info = {}

                location_text = (job_info.get('location') or '').strip()
                first_city_link = self.get_validated_city(location_text.split()[-1]) if location_text else first_city

                cities = [first_city] if first_city in romanian_cities else []

                additional_locations = job_info.get('additionalLocations') or []
                for city in additional_locations:
                    if isinstance(city, str) and city.strip():
                        loc = self.get_validated_city(city.split()[-1])
                        if loc in romanian_cities:
                            cities.append(loc)

                if first_city_link == 'Remote':
                    job_type = 'remote'

                if first_city_link in romanian_cities and first_city != first_city_link:
                    cities.append(first_city_link)

                self.get_jobs_dict(title, link, cities, job_type)
            except Exception:
                continue

        return self.jobs_list


blankfactor = Blankfactor(
    company_name='blankfactor',
    url='https://blankfactor.wd12.myworkdayjobs.com/wday/cxs/blankfactor/Blankfactor_External/jobs',
    logo_url='https://thepaymentsassociation.org/wp-content/uploads/sites/7/2023/07/Untitled-design-2023-07-24T151941.073.png'
)
blankfactor.get_jobs()
blankfactor.push_peviitor()
