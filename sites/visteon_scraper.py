from src.scrapers import Scraper


class Visteon(Scraper):

    def get_jobs(self):

        payload = {
        "opportunitySearch": {
            "Top": 50,
            "Skip": 0,
            "QueryString": "",
            "OrderBy": [
                {
                    "Value": "postedDateDesc",
                    "PropertyName": "PostedDate",
                    "Ascending": False
                }
            ],
            "Filters": [
                {
                    "t": "TermsSearchFilterDto",
                    "fieldName": 4,
                    "extra": None,
                    "values": ["7b452f5f-ff67-5d0c-96fa-21165e3a1824"]
                },
                {
                    "t": "TermsSearchFilterDto",
                    "fieldName": 5,
                    "extra": None,
                    "values": []
                },
                {
                    "t": "TermsSearchFilterDto",
                    "fieldName": 6,
                    "extra": None,
                    "values": []
                }
            ]
        },
        "matchCriteria": {
            "PreferredJobs": [],
            "Educations": [],
            "LicenseAndCertifications": [],
            "Skills": [],
            "hasNoLicenses": False,
            "SkippedSkills": []
        }
    }
        response = self.post_json(headers=self.headers, json=payload)['opportunities']

        for job in response:
            title = job['Title']
            link = (f"https://recruiting.ultipro.com/VIS1004VIST/JobBoard/6ea71e1c-667f-4ddc-9024-5966baaa3256/OpportunityDetail?opportunityId={job['Id']}")

            self.get_jobs_dict(title, link, 'Timisoara')

        return self.jobs_list


visteon = Visteon(
    company_name='visteon',
    url='https://recruiting.ultipro.com/VIS1004VIST/JobBoard/6ea71e1c-667f-4ddc-9024-5966baaa3256/JobBoardView/LoadSearchResults',
    logo_url='https://upload.wikimedia.org/wikipedia/commons/thumb/6/6a/Visteon_logo_%282016%29.svg/217px-Visteon_logo_%282016%29.svg.png'
)
visteon.get_jobs()
visteon.push_peviitor()
