from src.scrapers import Scraper


class Rws(Scraper):

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

        while True:
            soup = self.get_soup(params={
                'ss': '1',
                'in_iframe': '1',
                'searchLocation': '13526--Remote',
            })

            rows = soup.find_all('div', class_='row')
            found = False

            for row in rows:
                anchor = row.find('a', class_='iCIMS_Anchor')
                if not anchor:
                    continue

                full_title = anchor.get('title', '').strip()
                parts = full_title.split(' - ', 1)
                title = parts[1].strip() if len(parts) > 1 else full_title

                link = anchor.get('href', '')
                self.get_jobs_dict(title, link, 'Cluj-Napoca')
                found = True

            if not found:
                break

            paginator = soup.find('select', id='iCIMS_Paginator')
            if not paginator:
                break

            next_page = paginator.find('option', string=lambda s: s and s.strip().isdigit() and int(s.strip()) > 1)
            if not next_page:
                break

            self.url = next_page.get('value', self.url)

        return self.jobs_list


rws = Rws(
    company_name='rws',
    url='https://globalcareers-rws.icims.com/jobs/search',
    logo_url='https://c-13850-20230914-www-rws-com.i.icims.com/media/images/Artboard-1_tcm228-187294.svg?v=NjM4MjcwODY1NTA3MTQyMTkw',
)
rws.get_jobs()
rws.push_peviitor()
