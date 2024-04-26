from src.scrapers import Scraper


class Siena(Scraper):
    def __init__(self, company_name, url, logo_url):
        super().__init__(company_name, url, logo_url)

    def get_jobs(self):
        querystring = {"op": "ApiJobBoardWithTeams"}
        payload = {
            "operationName": "ApiJobBoardWithTeams",
            "variables": {"organizationHostedJobsPageName": "siena"},
            "query": "query ApiJobBoardWithTeams($organizationHostedJobsPageName: String!) "
                     "{\n  jobBoard: jobBoardWithTeams"
                     "(\n    organizationHostedJobsPageName: $organizationHostedJobsPageName\n  )"
                     " {\n    teams {\n      id\n      name\n      parentTeamId\n      __typename\n    }"
                     "\n    jobPostings "
                     "{\n      id\n      title\n      teamId\n      "
                     "locationId\n      locationName\n      employmentType\n      secondaryLocations "
                     "{\n        ...JobPostingSecondaryLocationParts\n        __typename\n      }"
                     "\n      compensationTierSummary\n      __typename\n    }"
                     "\n    __typename\n  }\n}\n\nfragment JobPostingSecondaryLocationParts on JobPostingSecondaryLocation "
                     "{\n  locationId\n  locationName\n  __typename\n}"}

        response = self.post_json(headers=self.headers, json=payload, params=querystring
                                  )['data']['jobBoard']['jobPostings']

        for job in response:

            locations = job['secondaryLocations']
            cities = []
            title = job['title']
            link = f"https://jobs.ashbyhq.com/siena/{job['id']}?utm_source=zLmkeq71qy"
            first_city = job['locationName']

            if 'remote' in title.lower():
                job_type = 'remote'
            elif 'hybrid' in title.lower():
                job_type = 'hibrid'
            else:
                job_type = 'on-site'

            for location in locations:
                secondary_location = location['locationName']

                if 'Cluj' in secondary_location:
                    cities.append('Cluj-Napoca')
                if 'Bucharest' in secondary_location:
                    cities.append('Bucuresti')
                if 'Iasi' in secondary_location:
                    cities.append('Iasi')

            if first_city in ['Bucharest', 'Cluj', 'Iasi']:
                cities.append(self.get_validated_city(first_city))

            if cities:
                self.get_jobs_dict(title, link, cities, job_type)

        return self.jobs_list


siena = Siena(
    company_name='siena',
    url='https://jobs.ashbyhq.com/api/non-user-graphql',
    logo_url='https://app.ashbyhq.com/api/images/org-theme-wordmark/2dbfc236-5c7c-4a85-95e0-942e757542ee/e92203a5-67f3-4e3c-bd29-c43e5003276e.png'
)
siena.get_jobs()
siena.push_peviitor()