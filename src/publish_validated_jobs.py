import requests
from county import get_county
import json
from update_peviitor import UpdatePeViitor


def publish_validated_jobs(company):

    token_ = UpdatePeViitor()
    access_token = token_.get_token()
    url_publish = "https://api.laurentiumarian.ro/jobs/publish/"
    payload_publish = []
    unpublished_jobs = []
    all_jobs = []
    payload = {"company": f"{company}"}
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    page = 1

    while True:
        response = requests.request("POST", "https://api.laurentiumarian.ro/jobs/get/",
                                    json=payload, headers=headers, params={"page":f"{page}"}).json()
        jobs = response['results']
        all_jobs.extend(jobs)
        next_page = response['next']

        if next_page is None:
            break

        page += 1

    for job in all_jobs:
        if job['published'] is False:
            unpublished_jobs.append(job)

    #print('unpublished_jobs ', len(unpublished_jobs))

    for item in unpublished_jobs:
        title = item.get('job_title')
        try:
            response_text = requests.get(item.get('job_link')).text
        except:
            response_text = None

        pass_title = True if title in response_text else False

        cities = item['city']
        pass_city = True
        for city in cities:
            if get_county(city) is None:
                pass_city = False

        if pass_title and pass_city:
            payload_publish.append(item)

    if len(payload_publish) > 0:
        response = requests.request("POST", url_publish, data=json.dumps(payload_publish), headers=headers)
        return print(response, response.text)

#publish_validated_jobs('Ceragon')
