from bs4 import BeautifulSoup
import requests
from .county import get_county
import re
from .update_peviitor import UpdatePeViitor
from .validate_city import validate_city


class Scraper:
    def __init__(self, company_name, url, logo_url=None):
        self.company_name = company_name
        self.url = url
        self.logo_url = logo_url
        self.jobs_list = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
            'Refer': 'https://google.com',
            'DNT': '1'
        }

    def get_soup(self, params=None):
        response = requests.get(self.url, headers=self.headers, params=params)
        soup = BeautifulSoup(response.text, 'lxml')
        return soup

    def get_link_soup(self, link):
        response = requests.get(url=link, headers=self.headers)
        soup = BeautifulSoup(response.text, 'lxml')
        return soup

    def get_json_link(self, link):
        response = requests.get(url=link, headers=self.headers).json()
        return response

    def get_json(self, json=None, data=None, params=None, headers=None):
        headers = self.headers if headers is None else headers
        response = requests.get(self.url, headers=headers, json=json, data=data, params=params).json()
        return response

    def post_json(self, headers=None, json=None, data=None, params=None):
        response = requests.post(self.url, headers=headers, json=json, data=data, params=params).json()
        return response

    def post_html(self, headers=None, data=None, params=None):
        response = requests.post(self.url,  headers=headers, data=data, params=params)
        soup = BeautifulSoup(response.text, 'lxml')
        return soup


    def get_cookies(self, *args):
        response = requests.head(self.url, headers=self.headers).headers
        cookies = {}
        for arg in args:
            match = re.search(f'({arg})=([^;]+);', str(response))
            if match:
                cookie_name = match.group(1)
                cookie_value = match.group(2)
                cookies[cookie_name] = cookie_value
            else:
                return None

        data = {
            "cookie": "; ".join([f"{name}={value}" for name, value in cookies.items()]),
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
        }

        return data


    @staticmethod
    def get_validated_city(city):
        return validate_city(city)

    def get_jobs_dict(self, job_title, job_link, city, remote='on-site', county=None):

        self.jobs_list.append({
            "job_title": job_title,
            "job_link": job_link,
            "company": self.company_name,
            "country": 'Romania',
            "county": county if county else get_county(city),
            "city": city,
            "remote": remote
        })

    def push_peviitor(self):
        UpdatePeViitor().update_jobs(self.company_name, self.jobs_list)
        UpdatePeViitor().update_logo(self.company_name, self.logo_url)

