import string
import random

import errno
import os
import datetime
import requests

curDir = os.getcwd()
dirName = os.path.join(curDir, datetime.datetime.now().strftime('%Y-%m-%d'))

if not os.path.exists(dirName):
    os.mkdir(dirName)
    print("Directory " , dirName ,  " Created ")
else:
    print("Directory " , dirName ,  " already exists")

os.chdir(dirName)

BASE_URL = 'https://i.imgur.com/'

def get_url():
    counter = 0
    url_hash = ''
    while counter < 5:
        random_letter = random.choice(string.ascii_letters)
        url_hash += random_letter
        counter += 1
    return BASE_URL + url_hash + '.jpg'


print('START')

while True:
    img_url = get_url()
    i = requests.get(img_url + '.jpg', stream=True)

    while i.url == 'https://i.imgur.com/removed.png':
        img_url = get_url()
        img = requests.get(img_url, stream=True)

    filename = img_url.split("/")[-1]

    r = requests.post(
        "https://api.deepai.org/api/nsfw-detector",
        data={
            'image': img_url + '.jpg',
        },
        headers={'api-key': 'your_api_key'}
    )
    json_response = r.json()
    print(json_response)
    if len(json_response['output']['detections']):
        print('Saving: ' + img_url + ' ...')
        image = requests.get(img_url)
        with open(filename, wb) as f:
            f.write(r.content)

