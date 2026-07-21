import html as html_mod
import json
from src.scrapers import Scraper
from src.validate_city import validate_city


class Teva(Scraper):

    def get_jobs(self):
        try:
            response = self.get_soup(verify=False)
        except Exception:
            return self.jobs_list

        positions = self._extract_positions(str(response))

        for job in positions:
            city_raw = job.get('location', '').split(',')[0].strip()
            city = validate_city(city_raw) if city_raw else 'Bucuresti'
            title = job.get('name', '').strip()
            link = job.get('canonicalPositionUrl', '')

            self.get_jobs_dict(title, link, city)

        return self.jobs_list

    @staticmethod
    def _extract_positions(raw_html):
        decoded = html_mod.unescape(raw_html)
        idx = decoded.find('"positions"')
        if idx < 0:
            return []

        arr_start = decoded.find('[', idx)
        if arr_start < 0:
            return []

        depth = 0
        for i in range(arr_start, len(decoded)):
            if decoded[i] == '[':
                depth += 1
            elif decoded[i] == ']':
                depth -= 1
                if depth == 0:
                    try:
                        return json.loads(decoded[arr_start:i + 1])
                    except json.JSONDecodeError:
                        return []
        return []


teva = Teva(
    company_name='teva',
    url='https://www.careers.teva/careers?domain=tevapharm.com&location=Romania&sort_by=relevance',
    logo_url='https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Teva_Pharmaceuticals_logo.png/800px-Teva_Pharmaceuticals_logo.png'
)
teva.get_jobs()
teva.push_peviitor()
