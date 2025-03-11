from src.county import get_county
from src.scrapers import Scraper


class Adecco(Scraper):

    def get_jobs(self):

        flag = True
        page = 0
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "ro-RO,ro;q=0.9,en-US;q=0.8,en;q=0.7",
            "Content-Type": "text/plain;charset=UTF-8",
            "Origin": "https://www.adecco.com",
            "Referer": "https://www.adecco.com/",
            "Sec-Ch-Ua": '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133")',
            "Sec-Ch-Ua-Mobile": "?1",
            "Sec-Ch-Ua-Platform": '"Android"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Mobile Safari/537.36",
            "Cookie": "jobSearchLogId=114983b4-5226-483c-8088-a92a73fdf5c3; OptanonAlertBoxClosed=2025-02-18T16:44:14.577Z;"
        }

        while flag:
            data = {
                "queryString": "&sort=PostedDate desc&facet.pivot=IsRemote&facet.range=Salary_Facet_Yearly&f.Salary_Facet_Yearly.facet.range.start=0&f.Salary_Facet_Yearly.facet.range.end=10000000&f.Salary_Facet_Yearly.facet.range.gap=500&facet.range=Salary_Facet_Hourly&f.Salary_Facet_Hourly.facet.range.start=0&f.Salary_Facet_Hourly.facet.range.end=850&f.Salary_Facet_Hourly.facet.range.gap=5",
                "filtersToDisplay": "{B3091B73-0670-4489-9491-0CB1FDACB021}|{3C1D2C5E-5E0E-4E54-874E-30752F246259}|{E4A1B922-5881-4773-8770-9415A7B4EC1B}|{2AD4E571-7E6E-4078-ACEF-8F4EA3597C30}|{50B4FD51-B765-4DF6-ACC9-90C51968A8C3}",
                "range": page, "siteName": "adecco", "brand": "adecco", "countryCode": "RO", "languageCode": "ro-RO"}

            jobs = self.post_json(headers, data).get("jobs")

            if jobs:

                for job in jobs:
                    title = job.get('jobTitle')
                    link = f"https://www.adecco.com/ro-ro/job-search/asistent-manager-cluj-napoca-cluj/{job.get('jobId')}"
                    city = self.get_validated_city(job.get('jobLocation'))
                    county = get_county(city)

                    self.get_jobs_dict(title, link, city,county=county)
                page += 10
            else:
                flag = False

        return self.jobs_list


adecco = Adecco(
    url="https://www.adecco.com/api/data/jobs/summarized",
    company_name='adecco',
    logo_url=''
)
adecco.get_jobs()
adecco.push_peviitor()

