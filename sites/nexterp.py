import re

from urllib.parse import urljoin

from src.scrapers import Scraper


class Nexterp(Scraper):

    def get_jobs(self):
        try:
            soup = self.get_soup()
            grid = soup.select_one('#jobs_grid') or soup
            seen = set()
            for job in grid.find_all('a', href=True):
                if not re.search(r'/jobs/(?:detail/|apply/)?[^/?#]+', job['href']):
                    continue
                link = urljoin(self.url, job['href'])
                if link in seen:
                    continue
                seen.add(link)

                title_tag = job.find(['h1', 'h2', 'h3', 'h4', 'h5']) or job
                title = title_tag.get_text(' ', strip=True)
                if not title:
                    continue

                self.get_jobs_dict(title, link, self.get_city(link))
        except Exception as e:
            print(f"Error while scraping {self.company_name}: {e}")

        return self.jobs_list

    def get_city(self, link):
        try:
            detail = self.get_link_soup(link)
            for selector in (
                'div.d-flex.align-items-baseline',
                '[itemprop="address"]',
                '.oe_place',
                'h5.text-center',
            ):
                node = detail.select_one(selector)
                if node:
                    city = node.get_text(' ', strip=True)
                    if city:
                        return city.split(',')[0].strip()
        except Exception:
            pass

        return ''


nexterp = Nexterp(
    company_name="NextERP",
    url="https://www.nexterp.ro/ro/jobs",
    logo_url=''

)
nexterp.get_jobs()
nexterp.push_peviitor()
