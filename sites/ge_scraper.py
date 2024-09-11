from src.scrapers import Scraper


class GeneralElectric(Scraper):

    def get_jobs(self):

        headers = self.get_cookies('PLAY_SESSION', 'PHPPPE_ACT')

        payload = {
            "lang": "en_global",
            "deviceType": "desktop",
            "country": "global",
            "pageName": "search-results",
            "ddoKey": "refineSearch",
            "sortBy": "",
            "subsearch": "",
            "from": 0,
            "jobs": True,
            "counts": True,
            "all_fields": ["business", "category", "jobFamilies", "country", "state", "city", "checkRemote", "experienceLevel"],
            "size": 20,
            "clearAll": False,
            "jdsource": "facets",
            "isSliderEnable": False,
            "pageId": "page1261",
            "siteType": "",
            "keywords": "",
            "global": True,
            "selected_fields": {"country": ["Romania"]},
            "locationData": {}
        }
        jobs = self.post_json(json=payload, headers=headers)['refineSearch']['data']['jobs']

        for job in jobs:
            title = job['title']
            city = self.get_validated_city(job['city'])
            link = f"https://jobs.gecareers.com/aviation/global/en/job/{job['jobId']}/"
            self.get_jobs_dict(title, link, city)

        return self.jobs_list

ge = GeneralElectric(
    url='https://jobs.gecareers.com/aviation/widgets',
    company_name='ge',
    logo_url=''
)
ge.get_jobs()
ge.push_peviitor()
