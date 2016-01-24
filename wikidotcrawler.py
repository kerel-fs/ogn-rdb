import requests
import random


def fetch_page(url, page_id):
    token = "".join(random.choice('abcdefghijklmnopqrstuvwxyz0123456789') for i in range(8))
    cookies = {"wikidot_token7": token}
    params = {"page_id": page_id,
              "moduleName": "viewsource/ViewSourceModule",
              "callbackIndex": 1,
              "wikidot_token7": token}
    req = requests.request('POST', url, data=params, cookies=cookies)
    return req.json()['body']
