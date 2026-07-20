from src.scrapers import Scraper

ROMANIA_ID = '81fca7f7-a70b-4568-ad38-318aaf996f55'


class Siena(Scraper):

    def get_jobs(self):
        payload = {
            "operationName": "ApiJobBoardWithTeams",
            "variables": {"organizationHostedJobsPageName": "siena"},
            "query": (
                "query ApiJobBoardWithTeams($organizationHostedJobsPageName: String!) {"
                "  jobBoard: jobBoardWithTeams(organizationHostedJobsPageName: $organizationHostedJobsPageName) {"
                "    jobPostings {"
                "      id title locationId locationName"
                "      secondaryLocations { locationId locationName __typename }"
                "      __typename"
                "    }"
                "    __typename"
                "  }"
                "}"
            ),
        }

        response = self.post_json(
            headers=self.headers,
            json=payload,
            params={"op": "ApiJobBoardWithTeams"},
        )

        postings = response['data']['jobBoard']['jobPostings']

        for job in postings:
            if not self._has_romania(job):
                continue

            title = job['title']
            link = f"https://jobs.ashbyhq.com/siena/{job['id']}"
            self.get_jobs_dict(title, link, 'Bucuresti')

        return self.jobs_list

    @staticmethod
    def _has_romania(job):
        if job.get('locationId') == ROMANIA_ID:
            return True
        return any(
            sl.get('locationId') == ROMANIA_ID
            for sl in job.get('secondaryLocations', [])
        )


siena = Siena(
    company_name='siena',
    url='https://jobs.ashbyhq.com/api/non-user-graphql',
    logo_url='https://app.ashbyhq.com/api/images/org-theme-wordmark/2dbfc236-5c7c-4a85-95e0-942e757542ee/e92203a5-67f3-4e3c-bd29-c43e5003276e.png'
)
siena.get_jobs()
siena.push_peviitor()
