from numpy.core.defchararray import title

from src.scrapers import Scraper


class Xylem(Scraper):
    def __init__(self, company_name, url, logo_url):
        super().__init__(company_name, url, logo_url)

    def get_jobs(self):

        payload = {
            "appliedFacets": {"locationCountry": ["f2e609fe92974a55a05fc1cdc2852122"]},
            "limit": 20,
            "offset": 0,
            "searchText": ""
        }
        headers = self.get_cookies("wd-browser-id", "PLAY_SESSION", "wday_vps_cookie", "__cf_bm", "__cflb", "_cfuvid")
        jobs = self.post_json(headers=headers, json=payload)['jobPostings']

        for job in jobs:
            title = job['title']
            link = "https://xylem.wd5.myworkdayjobs.com/en-US/xylem-careers" + job['externalPath']
            link_job_type = "https://xylem.wd5.myworkdayjobs.com/wday/cxs/xylem/xylem-careers"
            job_type = "hybrid" if self.get_json_link(link_job_type + job['externalPath'])['jobPostingInfo'].get('remoteType') \
                else "on-site"
            self.get_jobs_dict(title, link, "Bucuresti", job_type)

        return self.jobs_list



xylem = Xylem(
    company_name='xylem',
    url='https://xylem.wd5.myworkdayjobs.com/wday/cxs/xylem/xylem-careers/jobs',
    logo_url='https://www.xylem.com/siteassets/brand/_logos/color-lockups-transparent/xylem_tag_7704c.svg'
)

xylem.get_jobs()
xylem.push_peviitor()
