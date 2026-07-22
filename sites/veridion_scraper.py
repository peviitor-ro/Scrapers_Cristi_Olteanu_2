from src.scrapers import Scraper
from src.validate_city import validate_city


class Veridion(Scraper):

    def get_jobs(self):
        response = self.get_soup()

        for a in response.find_all('a', href=True):
            href = a['href']
            if not href.startswith('/company/careers/') or href == '/company/careers':
                continue

            title_el = a.find('h3', attrs={'data-slot': 'tile-title'})
            if not title_el:
                continue
            title = title_el.text.strip()

            location_el = a.find('span', class_='text-label-md')
            location_text = location_el.text.strip() if location_el else ''
            parts = [p.strip() for p in location_text.split('·')]
            city = validate_city(parts[-1]) if parts else 'Bucuresti'

            work_el = a.find('span', class_='inline-flex')
            work_text = work_el.text.strip().lower() if work_el else 'on-site'
            job_type = 'hybrid' if 'hybrid' in work_text else 'on-site'

            link = 'https://veridion.com' + href
            county = city

            self.get_jobs_dict(title, link, city, job_type, county=county)

        return self.jobs_list


veridion = Veridion(
    company_name='veridion',
    url='https://veridion.com/careers/',
    logo_url='https://veridion.com/wp-content/themes/soleadify/assets/images/graphical-elements/main-logo.png'
)
veridion.get_jobs()
veridion.push_peviitor()
