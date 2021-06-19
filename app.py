import requests
from flask import Flask, render_template

import config

app = Flask(__name__)


@app.route('/')
def index():
    data = get_data()
    dogs_districts_dict = data_to_dict(data)
    return render_template('index.html', data=dogs_districts_dict)


def get_data():
    rows_url = config.API_MAIN_URL + 'datasets/2663/rows'
    count_url = config.API_MAIN_URL + 'datasets/2663/count'

    r = requests.get(count_url, params={'api_key': config.API_KEY})

    limit = int(r.text)
    skip = 0
    step = 100

    data = []
    while len(data) < limit:
        params = {
            '$top': step,
            '$skip': skip,
            'api_key': config.API_KEY,
        }

        r = requests.get(rows_url, params=params)

        j = r.json()

        for element in j:
            data.append(element)
        skip += step

    return data

def data_to_dict(data):
    dogs_districts_dict = {}

    for element in data:
        if "Cells" in element:
            district = element["Cells"]["District"]
        if district in dogs_districts_dict:
            dogs_districts_dict[district] += 1
        else:
            dogs_districts_dict[district] = 1

    return dogs_districts_dict

if __name__ == '__main__':
    app.run()
