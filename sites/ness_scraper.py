import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

from src.scrapers import Scraper


class Ness(Scraper):

    def get_jobs(self):
        page = 1
        flag = True

        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36')

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        while flag:
            try:
                url = f'https://ness-usa.ttcportals.com/search/jobs/in/country/romania?page={page}'
                driver.get(url)
                time.sleep(3)

                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "jobs-section__item"))
                )

                soup = self.soup(driver.page_source)
                jobs = soup.find_all('div', class_='jobs-section__item padded-v-small')

                if len(jobs) > 0:
                    for job in jobs:
                        title = job.find('a').text.strip()
                        link = job.find('a')['href']
                        city = job.find('div', class_='large-4 columns').text.split('Location:')[-1].split(',')[0].strip().rstrip('.')
                        city = self.get_validated_city(city)
                        self.get_jobs_dict(title, link, city)

                    page += 1
                else:
                    flag = False
            except Exception:
                flag = False

        driver.quit()
        return self.jobs_list

    @staticmethod
    def soup(html):
        from bs4 import BeautifulSoup
        return BeautifulSoup(html, 'lxml')

ness = Ness(
    company_name='ness',
    url='https://ness-usa.ttcportals.com/search/jobs/in/country/romania',
    logo_url='https://ness-usa.ttcportals.com/system/production/assets/357234/original/Ness--logo.png'
)
ness.get_jobs()
ness.push_peviitor()