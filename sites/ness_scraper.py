from src.scrapers import Scraper


class Ness(Scraper):

    def get_jobs(self):
        page = 1
        flag = True

        while flag:

            response = self.get_link_soup(f'https://ness-usa.ttcportals.com/search/jobs/in/country/romania?page={page}#')
            jobs = response.find_all('div', class_='jobs-section__item padded-v-small')

            if len(jobs) > 0:

                for job in jobs:
                    title = job.find('a').text
                    link = job.find('a')['href']
                    city = job.find('div', class_='large-4 columns').text.split('Location:')[-1].split(',')[0].strip()
                    self.get_jobs_dict(title, link, city)

                page += 1
            else:
                flag = False

        return self.jobs_list

ness = Ness(
    company_name='ness',
    url='https://ness-usa.ttcportals.com/search/jobs/in/country/romania',
    logo_url='https://ness-usa.ttcportals.com/system/production/assets/357234/original/Ness--logo.png'
)
ness.get_jobs()
ness.push_peviitor()
