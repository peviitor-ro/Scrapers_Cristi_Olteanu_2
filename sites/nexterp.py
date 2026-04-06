from src.scrapers import Scraper


class Nexterp(Scraper):

    def get_jobs(self):
        try:
            jobs = self.get_soup().find_all('a', class_='text-decoration-none')
            for job in jobs:
                link = "https://www.nexterp.ro" + job.get('href')
                title = job.find('h3').text.strip()
                city = self.get_link_soup(link).find('div', class_='d-flex align-items-baseline').text.split(',')[0].strip()
                self.get_jobs_dict(title, link, city)
        except Exception as e:
            print(f"Error while scraping {self.company_name}: {e}")

        return self.jobs_list


nexterp = Nexterp(
    company_name="NextERP",
    url="https://www.nexterp.ro/ro/jobs",
    logo_url=''

)
nexterp.get_jobs()
nexterp.push_peviitor()
