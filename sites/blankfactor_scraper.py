from src.scrapers import Scraper


class Blankfactor(Scraper):

    def get_jobs(self):
        headers = self.get_cookies('wd-browser-id', 'PLAY_SESSION', 'wday_vps_cookie', 'vps-cke', '__cf_bm', '__cflb', '_cfuvid')
        if not headers:
            headers = self.headers.copy()
            headers['Content-Type'] = 'application/json'
            headers['Accept'] = 'application/json'

        jobs = []
        offset = 0
        while True:
            payload = {
                "appliedFacets": {},
                "limit": 20,
                "offset": offset,
                "searchText": ""
            }
            try:
                response = self.post_json(headers=headers, json=payload)
            except Exception:
                break
            if not isinstance(response, dict):
                break
            postings = response.get('jobPostings') or []
            jobs.extend(postings)
            offset += len(postings)
            total = response.get('total')
            if not postings or len(postings) < payload['limit'] or (isinstance(total, int) and total > 0 and offset >= total):
                break

        romanian_cities = ['Cluj-Napoca', 'Bucuresti']
        for job in jobs:
            try:
                job_type = 'on-site'
                title = job['title']
                link = f"https://blankfactor.wd12.myworkdayjobs.com/en-US/Blankfactor_External{job['externalPath']}"
                link_info = f"https://blankfactor.wd12.myworkdayjobs.com/wday/cxs/blankfactor/Blankfactor_External{job['externalPath']}"

                try:
                    job_info = self.get_json_link(link_info).get('jobPostingInfo', {})
                except Exception:
                    job_info = {}

                location_text = (job_info.get('location') or '').strip()
                if 'remote' in location_text.lower():
                    job_type = 'remote'

                locations = [job.get('locationsText'), location_text]
                locations.extend(job_info.get('additionalLocations') or [])
                cities = []
                for location in locations:
                    if not isinstance(location, str) or not location.strip():
                        continue
                    candidates = [location, location.replace('-', ' '), location.split(',')[0].strip(), location.split()[-1] if location.split() else '']
                    for candidate in candidates:
                        city = self.get_validated_city(candidate)
                        if city in romanian_cities and city not in cities:
                            cities.append(city)

                for city in cities:
                    self.get_jobs_dict(title, link, city, job_type)
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
