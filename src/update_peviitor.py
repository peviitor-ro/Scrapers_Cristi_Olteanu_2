import requests
import os
import json
import time


class UpdatePeViitor:

    def __init__(self):
        self.post_url = 'https://api.peviitor.ro/v5/add/'
        self.logo_url = 'https://api.peviitor.ro/v1/logo/add/'

        self.post_header = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.get_token()}'
        }

        self.logo_header = {
            'Content-Type': 'application/json',
        }


    def get_token(self):
        token_endpoint = 'https://api.peviitor.ro/v5/get_token/'

        token = requests.post(token_endpoint, data={
            "email": 'cristiolteanu1892@gmail.com'
        })

        return token.json()['access']


    def update_jobs(self, company_name: str, data_jobs: list):


        # time sleep for SOLR indexing
        time.sleep(0.2)

        post_request_to_server = requests.post(self.post_url, headers=self.post_header,
                                               data=json.dumps(data_jobs))



    def update_logo(self, id_company: str, logo_link: str):

        data = json.dumps([{"id": id_company, "logo": logo_link}])
        response = requests.post(self.logo_url, headers=self.logo_header, data=data)



