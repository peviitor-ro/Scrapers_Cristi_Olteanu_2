from src.scrapers import Scraper


class Dennemeyer(Scraper):

    def get_jobs(self):
        payload = {
            "appliedFacets": {"locations": ["08c8c9a677fd1001ea92225ba5d90000", "99c9060b642e1001e86635de40a00000",
                                            "023dd96435d8016f98adf461d036dbdb"]},
            "limit": 20,
            "offset": 0,
            "searchText": ""
        }
        headers = self.get_cookies('PLAY_SESSION', 'wd-browser-id', 'wday_vps_cookie', '__cf_bm', '__cflb', '__cflb')

        jobs = self.post_json(headers, payload)['jobPostings']

        for job in jobs:
            title = job['title']
            link = f"https://dennemeyer.wd3.myworkdayjobs.com/en-US/dennemeyer_careers{job['externalPath']}"
            self.get_jobs_dict(title, link, 'Brasov')

        return self.jobs_list


dennemeyer = Dennemeyer(
    url='https://dennemeyer.wd3.myworkdayjobs.com/wday/cxs/dennemeyer/dennemeyer_careers/jobs',
    company_name='dennemeyer',
    logo_url=''
)
dennemeyer.get_jobs()
dennemeyer.push_peviitor()
