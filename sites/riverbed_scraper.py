from src.scrapers import Scraper
from src.validate_city import validate_city


class Riverbed(Scraper):

    def get_jobs(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9,ro;q=0.8',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
        }

        page = 1
        while True:
            soup = self.get_soup(params={
                'ss': '1',
                'searchLocation': '13526',
                'in_iframe': '1',
            })

            rows = soup.find_all('div', class_='row')
            found = False

            for row in rows:
                h3 = row.find('h3')
                if not h3:
                    continue

                parent_a = h3.find_parent('a')
                if not parent_a:
                    continue

                link = parent_a.get('href', '')
                title = h3.text.strip()

                location_span = row.find('span', string=lambda s: s and 'RO-' in s)
                if not location_span:
                    continue

                location_text = location_span.text.strip()
                city_raw = location_text.split('RO-')[-1].strip()
                city = validate_city(city_raw)

                self.get_jobs_dict(title, link, city)
                found = True

            if not found:
                break

            paginator = soup.find('select', id='iCIMS_Paginator')
            if not paginator:
                break

            options = paginator.find_all('option')
            next_option = None
            for opt in options:
                if opt.text.strip() == str(page + 1):
                    next_option = opt
                    break

            if not next_option:
                break

            self.url = next_option.get('value', self.url)
            page += 1

        return self.jobs_list


riverbed = Riverbed(
    url='https://emea-apj-riverbed.icims.com/jobs/search',
    company_name='riverbed',
    logo_url='https://cms.jibecdn.com/prod/riverbed/assets/HEADER-LOGO_IMG-en-us-1649182997894.png'
)
riverbed.get_jobs()
riverbed.push_peviitor()
