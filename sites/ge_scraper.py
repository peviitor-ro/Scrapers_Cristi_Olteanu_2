from src.scrapers import Scraper


class GeneralElectric(Scraper):

    def get_jobs(self):

        headers = self.get_cookies('PLAY_SESSION', 'PHPPPE_ACT')

        payload = {
            "sortBy": "",
            "subsearch": "",
            "from": 0,
            "jobs": True,
            "counts": True,
            "all_fields": ["category", "jobFamilies", "country", "state", "city", "checkRemote", "experienceLevel"],
            "pageName": "search-results",
            "size": 10,
            "clearAll": False,
            "jdsource": "facets",
            "isSliderEnable": False,
            "pageId": "page20",
            "siteType": "external",
            "keywords": "",
            "global": True,
            "selected_fields": {"country": ["Romania"]},
            "lang": "en_global",
            "deviceType": "mobile",
            "country": "global",
            "refNum": "GAOGAYGLOBAL",
            "ddoKey": "refineSearch"
        }
        jobs = self.post_json(json=payload, headers=headers)['refineSearch']['data']['jobs']

        for job in jobs:
            title = job['title']
            city = self.get_validated_city(job['city'])
            link = f"https://jobs.gecareers.com/aviation/global/en/job/{job['jobId']}/"
            self.get_jobs_dict(title, link, city)

        return self.jobs_list

ge = GeneralElectric(
    url='https://careers.geaerospace.com/widgets',
    company_name='ge',
    logo_url=''
)
ge.get_jobs()
ge.push_peviitor()
