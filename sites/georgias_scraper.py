from src.scrapers import Scraper


class Georgias(Scraper):

    def get_jobs(self):
        querystring = {"op": "ApiJobBoardWithTeams"}
        payload = "{\"operationName\":\"ApiJobBoardWithTeams\",\"variables\":{\"organizationHostedJobsPageName\":\"gorgias\"},\"query\":\"query ApiJobBoardWithTeams($organizationHostedJobsPageName: String!) {\\n  jobBoard: jobBoardWithTeams(\\n    organizationHostedJobsPageName: $organizationHostedJobsPageName\\n  ) {\\n    teams {\\n      id\\n      name\\n      parentTeamId\\n      __typename\\n    }\\n    jobPostings {\\n      id\\n      title\\n      teamId\\n      locationId\\n      locationName\\n      employmentType\\n      secondaryLocations {\\n        ...JobPostingSecondaryLocationParts\\n        __typename\\n      }\\n      compensationTierSummary\\n      __typename\\n    }\\n    __typename\\n  }\\n}\\n\\nfragment JobPostingSecondaryLocationParts on JobPostingSecondaryLocation {\\n  locationId\\n  locationName\\n  __typename\\n}\"}"
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36"
        }
        jobs = self.post_json(headers=headers,data=payload, params=querystring)['data']['jobBoard']['jobPostings']

        for job in jobs:
            link = f"https://www.gorgias.com/about-us/jobs?ashby_jid={job['id']}"
            title = job['title']
            primary_location = job['locationName']
            secondary_Locations = job['secondaryLocations']

            if 'Bucharest' in primary_location:
                city = 'Bucuresti'
            elif secondary_Locations and 'Bucharest' in secondary_Locations[0]['locationName']:
                city = 'Bucuresti'
            else:
                city = None

            if city:
                self.get_jobs_dict(title, link, city)

        return self.jobs_list

georgias = Georgias(
    company_name='georgias',
    url='https://jobs.ashbyhq.com/api/non-user-graphql',
    logo_url='https://logowik.com/content/uploads/images/gorgias8627.jpg'
)
georgias.get_jobs()
georgias.push_peviitor()
