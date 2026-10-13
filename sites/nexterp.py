from urllib.parse import urljoin

from src.scrapers import Scraper


class Nexterp(Scraper):

    def get_jobs(self):
        try:
            soup = self.get_soup()
            jobs = soup.find_all('a', class_='text-decoration-none')
            for job in jobs:
                title_tag = job.find('h3')
                if not title_tag:
                    continue
                link = urljoin("https://www.nexterp.ro", job.get('href'))
                title = title_tag.text.strip()
                city_div = self.get_link_soup(link).find('div', class_='d-flex align-items-baseline')
                city = city_div.text.split(',')[0].strip() if city_div else ''
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
