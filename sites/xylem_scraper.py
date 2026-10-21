from src.scrapers import Scraper


class Xylem(Scraper):

    def get_jobs(self):
        headers = self.get_cookies("wd-browser-id", "PLAY_SESSION", "wday_vps_cookie", "__cf_bm", "__cflb", "_cfuvid")
        if not headers:
            headers = self.headers
            headers['Content-Type'] = 'application/json'

        all_jobs = []
        for offset in range(0, 1000, 20):
            payload = {
                "limit": 20,
                "offset": offset,
                "searchText": "",
                "appliedFacets": {}
            }
            try:
                response = self.post_json(headers=headers, json=payload)
                jobs = response.get('jobPostings', [])
                if not jobs:
                    break
                all_jobs.extend(jobs)
            except Exception:
                break

        for job in all_jobs:
            locations = job.get('locations') or []
            locations_str = str(locations).lower()
            if 'romania' not in locations_str and 'bucure' not in locations_str and 'bucharest' not in locations_str:
                continue
            title = job['title']
            link = "https://xylem.wd5.myworkdayjobs.com/en-US/xylem-careers" + job['externalPath']
            link_job_type = "https://xylem.wd5.myworkdayjobs.com/wday/cxs/xylem/xylem-careers"
            try:
                job_info = self.get_json_link(link_job_type + job['externalPath'])
                job_type = "hybrid" if job_info.get('jobPostingInfo', {}).get('remoteType') else "on-site"
            except Exception:
                job_type = "on-site"
            city = "Bucuresti"
            if locations and isinstance(locations, list) and locations:
                loc = locations[0]
                if isinstance(loc, dict):
                    city = loc.get('city') or loc.get('location') or "Bucuresti"
                elif isinstance(loc, str):
                    city = loc
            self.get_jobs_dict(title, link, city, job_type)

        return self.jobs_list



xylem = Xylem(
    company_name='xylem',
    url='https://xylem.wd5.myworkdayjobs.com/wday/cxs/xylem/xylem-careers/jobs',
    logo_url='https://www.xylem.com/siteassets/brand/_logos/color-lockups-transparent/xylem_tag_7704c.svg'
)

xylem.get_jobs()
xylem.push_peviitor()
