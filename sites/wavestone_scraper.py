import requests

from src.scrapers import Scraper


class WaveStone(Scraper):
    def __init__(self, company_name, url, logo_url):
        super().__init__(company_name, url, logo_url)

    def get_jobs(self):

        payload = {
            "userId": "2c2a4ca7-b744-48bb-a201-898565e05b60",
            "projectId": "6b078a44-931a-40b3-be4f-6e76f550f6df",
            "pageId": "ebeb3826-c6dd-4ac7-befa-d0b0ffde8515",
            "isStandalone": False,
            "locale": "en",
            "isActiveCustomJobPages": True,
            "isUseLayoutsOfSubsidiaries": False,
            "filterStatus": {
                "careerLevel": True,
                "category": False,
                "partnership": False,
                "location": True,
                "company": False
            },
            "pageNumber": 1,
            "numberOfJobsOnPage": 20,
            "listState": {
                "search": "",
                "location": {},
                "filters": {"location": ["Romania"]},
                "filterPredictions": {}
            },
            "jobListTitleNew": "New",
            "isGetFilters": True,
            "isForCurrentLocale": True
        }
        headers = {
            "authority": "pcw-api.softgarden.de",
            "method": "POST",
            "path": "/widget-api/job-list/jobAds/",
            "scheme": "https",
            "accept": "*/*",
            "content-type": "application/json",
            "origin": "https://romania-career.wavestone.com",
            "priority": "u=1, i",
            "referer": "https://romania-career.wavestone.com/",
            "sec-ch-ua": '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "cross-site",
            "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Mobile Safari/537.36"
        }

        jobs = self.post_json(json=payload, headers=headers)['data']['jobs']

        for job in jobs:
            title = job['title']
            link = 'https://romania-career.wavestone.com' + job['link']
            self.get_jobs_dict(title, link, 'Cluj-Napoca', 'hybrid', 'Cluj')

        return self.jobs_list


wavestone = WaveStone(
    company_name='wavestone',
    url='https://pcw-api.softgarden.de/widget-api/job-list/jobAds/',
    logo_url=''
)
wavestone.get_jobs()
wavestone.push_peviitor()
