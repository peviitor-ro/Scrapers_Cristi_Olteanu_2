import requests
import os
import json
import time


class UpdatePeViitor:

    def __init__(self):
        self.api_key = os.environ.get('API_KEY')
        self.clean_url = 'https://api.peviitor.ro/v4/clean/'
        self.post_url = 'https://api.peviitor.ro/v4/update/'
        self.logo_url = 'https://api.peviitor.ro/v1/logo/add/'

        self.clean_header = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'apikey': self.api_key
        }

        self.post_header = {
            'Content-Type': 'application/json',
            'apikey': self.api_key
        }

        self.logo_header = {
            'Content-Type': 'application/json',
        }

    def update_jobs(self, company_name: str, data_jobs: list):

        clean_request = requests.post(self.clean_url, headers=self.clean_header,
                                      data={'company': company_name})

        # time sleep for SOLR indexing
        time.sleep(0.2)

        post_request_to_server = requests.post(self.post_url, headers=self.post_header,
                                               data=json.dumps(data_jobs))

        # not delete this lines if you want to see the graph on scraper's page
        file = company_name.lower() + '_scraper.py'
        data = {'data': len(data_jobs)}
        dataset_url = f'https://dev.laurentiumarian.ro/dataset/Scrapers_Cristi_Olteanu/{file}/'
        requests.post(dataset_url, json=data)
        #######################################################################

        print(json.dumps(data_jobs, indent=4))

    def update_logo(self, id_company: str, logo_link: str):

        data = json.dumps([{"id": id_company, "logo": logo_link}])
        response = requests.post(self.logo_url, headers=self.logo_header, data=data)


