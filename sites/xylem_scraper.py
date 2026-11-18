from src.scrapers import Scraper


class Xylem(Scraper):

    def get_jobs(self):
        headers = self.get_cookies("wd-browser-id", "PLAY_SESSION", "wday_vps_cookie", "__cf_bm", "__cflb", "_cfuvid")
        if not headers:
            headers = self.headers
            headers['Content-Type'] = 'application/json'

        all_jobs = []
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
            all_jobs.extend(jobs)
            offset += len(jobs)
            total = response.get('total')
            if isinstance(total, int) and offset >= total:
                break

        for job in all_jobs:
            location_parts = [job.get('locationsText') or '']
            location_parts.extend(job.get('bulletFields') or [])
            locations_str = ' '.join(str(part) for part in location_parts).lower()
            if 'romania' not in locations_str and 'bucure' not in locations_str and 'bucharest' not in locations_str:
                continue
            title = job['title']
            external_path = job['externalPath']
            link = "https://xylem.wd5.myworkdayjobs.com/en-US/xylem-careers" + external_path
            link_job_type = "https://xylem.wd5.myworkdayjobs.com/wday/cxs/xylem/xylem-careers" + external_path
            try:
                job_info = self.get_json_link(link_job_type).get('jobPostingInfo', {})
            except Exception:
                job_info = {}
            remote_type = str(job_info.get('remoteType') or '').lower()
            if 'hybrid' in remote_type:
                job_type = 'hybrid'
            elif 'remote' in remote_type:
                job_type = 'remote'
            else:
                job_type = 'on-site'
            city = "Bucuresti"
            for part in location_parts:
                part = str(part)
                if 'bucure' in part.lower() or 'bucharest' in part.lower():
                    city = self.get_validated_city(part.split(',')[0].strip())
                    break
            self.get_jobs_dict(title, link, city, job_type)

        return self.jobs_list



xylem = Xylem(
    company_name='xylem',
    url='https://xylem.wd5.myworkdayjobs.com/wday/cxs/xylem/xylem-careers/jobs',
    logo_url='https://www.xylem.com/siteassets/brand/_logos/color-lockups-transparent/xylem_tag_7704c.svg'
)

xylem.get_jobs()
xylem.push_peviitor()
