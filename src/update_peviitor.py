import requests
import os
import json
import time


class UpdatePeViitor:

    def __init__(self):
        self.post_url = 'https://api.laurentiumarian.ro/jobs/add/'
        self.logo_url = 'https://api.peviitor.ro/v1/logo/add/'

        self.post_header = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.get_token()}',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
        }

        self.logo_header = {
            'Content-Type': 'application/json',
        }

    def get_token(self):
        #token_endpoint = 'https://api.peviitor.ro/v5/get_token/'
        token_endpoint = 'https://api.laurentiumarian.ro/get_token'

        token = requests.post(token_endpoint, json={
            "email": 'cristiolteanu1892@gmail.com'
        })
        return token.json()['access']


    def update_jobs(self, company, data_jobs: list):

        # time sleep for SOLR indexing
        time.sleep(0.2)

        res = requests.post(self.post_url, headers=self.post_header, data=json.dumps(data_jobs))
        print(res.status_code)
        print(json.dumps(data_jobs, indent=4))

    def update_logo(self, id_company: str, logo_link: str):

        data = json.dumps([{"id": id_company, "logo": logo_link}])
        #print(requests.post(self.logo_url, headers=self.logo_header, data=data))



