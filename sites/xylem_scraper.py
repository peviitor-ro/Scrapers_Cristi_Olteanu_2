from src.scrapers import Scraper


class Xylem(Scraper):

    def get_jobs(self):
        headers = self.get_cookies("wd-browser-id", "PLAY_SESSION", "wday_vps_cookie", "__cf_bm", "__cflb", "_cfuvid")
        if not headers:
            headers = self.headers
            headers['Content-Type'] = 'application/json'

        all_jobs = []
        facets = []
        offset = 0
        while True:
            payload = {
                "limit": 20,
                "offset": offset,
                "searchText": "",
                "appliedFacets": {}
            }
            try:
                response = self.post_json(headers=headers, json=payload)
            except Exception:
                break
            jobs = response.get('jobPostings', []) if isinstance(response, dict) else []
            if not jobs:
                break
            if not facets:
                facets = response.get('facets', [])
            all_jobs.extend(jobs)
            offset += len(jobs)
            total = response.get('total')
            if len(jobs) < payload['limit'] or (isinstance(total, int) and total > 0 and offset >= total):
                break

        romanian_jobs = []
        for job in all_jobs:
            location_parts = self.get_location_parts(job)
            locations_str = ' '.join(location_parts).lower()
            if any(word in locations_str for word in ('romania', 'bucure', 'bucharest')):
                romanian_jobs.append(job)
        jobs = romanian_jobs if romanian_jobs else all_jobs
        remote_types = self.get_remote_types(headers, facets)

        for job in jobs:
            location_parts = self.get_location_parts(job)
            locations_str = ' '.join(location_parts).lower()
            is_romanian = any(word in locations_str for word in ('romania', 'bucure', 'bucharest'))
            title = job['title']
            external_path = job['externalPath']
            link = "https://xylem.wd5.myworkdayjobs.com/en-US/xylem-careers" + external_path
            job_type = remote_types.get(external_path, 'on-site')
            city = self.get_city(location_parts, is_romanian)
            self.get_jobs_dict(title, link, city, job_type)

        return self.jobs_list

    @staticmethod
    def get_location_parts(job):
        parts = [str(job.get('locationsText') or '')]
        parts.extend(str(part) for part in (job.get('bulletFields') or []))
        return parts

    @staticmethod
    def get_city(location_parts, is_romanian):
        for part in location_parts:
            if 'bucure' in part.lower() or 'bucharest' in part.lower():
                return Xylem.get_validated_city(part.split(',')[0].strip())
        if is_romanian:
            return "Bucuresti"
        locations = location_parts[0]
        if 'locations' in locations.lower():
            locations = location_parts[1].split(';')[0].strip() if len(location_parts) > 1 else ''
        return locations.split(',')[0].strip() if locations else "Bucuresti"

    def get_remote_types(self, headers, facets):
        remote_types = {}
        for facet in facets:
            if facet.get('facetParameter') != 'remoteType':
                continue
            for option in facet.get('values', []):
                descriptor = str(option.get('descriptor') or '').lower()
                if 'hybrid' in descriptor:
                    remote_type = 'hybrid'
                elif 'remote' in descriptor:
                    remote_type = 'remote'
                else:
                    remote_type = 'on-site'
                offset = 0
                while True:
                    payload = {
                        "limit": 20,
                        "offset": offset,
                        "searchText": "",
                        "appliedFacets": {"remoteType": [option['id']]}
                    }
                    try:
                        response = self.post_json(headers=headers, json=payload)
                    except Exception:
                        break
                    postings = response.get('jobPostings', []) if isinstance(response, dict) else []
                    if not postings:
                        break
                    for posting in postings:
                        if posting.get('externalPath'):
                            remote_types[posting['externalPath']] = remote_type
                    offset += len(postings)
                    total = response.get('total')
                    if len(postings) < payload['limit'] or (isinstance(total, int) and total > 0 and offset >= total):
                        break
        return remote_types



xylem = Xylem(
    company_name='xylem',
    url='https://xylem.wd5.myworkdayjobs.com/wday/cxs/xylem/xylem-careers/jobs',
    logo_url='https://www.xylem.com/siteassets/brand/_logos/color-lockups-transparent/xylem_tag_7704c.svg'
)

xylem.get_jobs()
xylem.push_peviitor()
