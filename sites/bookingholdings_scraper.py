from src.scrapers import Scraper
from src.validate_city import validate_city


class BookingHoldings(Scraper):

    def get_jobs(self):
        flag = True
        page = 1

        while flag:
            querystring = {"locations": "Bucharest,Bucureşti,Romania", "page": f"{page}", "sortBy": "relevance",
                           "descending": "false", "internal": "false", "tags1": "Booking Holdings COE Company Hierarchy"}
            headers = self.get_cookies('session_id', 'jasession')

            jobs = self.get_json(headers=headers, params=querystring)['jobs']

            if jobs:

                for job in jobs:
                    job_title = job['data']['title']
                    job_city = validate_city(job['data']['location_name'].split('-')[0].strip())
                    job_link = f"https://www.bookingholdings-coe.com/bookingholdings-coe/jobs/{job['data']['req_id']}?lang=en-us"

                    self.get_jobs_dict(job_title, job_link, job_city)
            else:
                flag = False
            page += 1

        return self.jobs_list

booking_holdings = BookingHoldings(
    company_name='BookingHoldings',
    url='https://www.bookingholdings-coe.com/api/jobs'
    )
booking_holdings.get_jobs()
booking_holdings.push_peviitor()
