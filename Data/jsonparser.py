import json
import os
import requests
directory = 'C:\Users\mariam.riaz\PycharmProjects\Scientific-Paper-Summarizer\Data\fullpapers'

for filename in os.listdir(directory):
    url = 'http://localhost:8080/v1'
    headers = {'Content-type': 'application/pdf', 'Accept-Charset': 'UTF-8'}
    data = open(filename, 'rb')
    r = requests.post(url, data=data, headers=headers)
    data2 = r.json()
    paper = data2['title']
    json_file = paper+'.json'
    with open(paper+'.json', 'w') as json_file:
        json.dump(data2, f)