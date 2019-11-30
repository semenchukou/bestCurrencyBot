import requests
import urllib.request
from bs4 import BeautifulSoup
from matplotlib import pyplot as plt
import io

api_key = '86cdb721-85dc-4543-82cc-da31de3d9c96'

def get_html(url):
    response = urllib.request.urlopen(url)
    return response.read()

def extract_lat_long_via_address(address):
    lat, lng = None, None
    url = "https://geocode-maps.yandex.ru/1.x/?format=json&apikey=" + api_key + "&geocode=" + address
    resp = requests.get(url)
    data = resp.json()
    return data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'].split(' ')

def parse_for_best_values(url, to_buy):
    soup = BeautifulSoup(get_html(url))
    table = soup.find("table", {'class' : 'tbl-lite banks-table'}).find('tbody')
    fitting_row = table.find("tr")
    parts = fitting_row.findAll("td")
    name = parts[0].find('p').text
    value = 0.0
    if to_buy == True:
        value = float(parts[1].find('span').text)
    else:
        value = float(parts[2].find('span').text)
    address = parts[3].find('a').text
    
    return name, value, address

def parse_for_history_and_build_figure(url, currency):
    soup = BeautifulSoup(get_html(url))
    dates = []
    rates = []
    table = soup.find("table", {'class' : 'tbl-lite m-archive-currencies'}).find('tbody')
    rows = table.findAll("tr")
    for row in rows:
        parts = row.findAll("td")
        dates.append(parts[0].text)
        rates.append(float(parts[1].text))
    dates.reverse()
    rates.reverse()
    plt.plot(dates, rates)
    plt.title('Rates history for ' + currency)
    plt.xlabel("Dates")
    plt.ylabel("Rates")
    plt.tick_params(axis = 'x', rotation = 270)
    plt.tight_layout()
    buf = io.BytesIO()
    buf.name = 'image.jpeg'
    plt.savefig(buf, format='png')
    buf.seek(0)
    return buf