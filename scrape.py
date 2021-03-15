import requests
import random
from bs4 import BeautifulSoup

def rarity_color(rarity_classes=None):
    rarity_table = {
        'legendary': 0xFFDA87,
        'epic': 0x9400D3,
        'rare': 0x1E4ED1,
        'common': 0x6e7c7c,
    }

    for rarity_class in rarity_classes:
        if rarity_class in rarity_table.keys():
            rarity = rarity_table[rarity_class]
        else:
            rarity = rarity_table['common']
    return rarity

def scrape_pixel_random():
    url = 'https://www.mypixelplanet.com/'
    page = random.choice(('', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'))
    html = BeautifulSoup(requests.get(url+page).text, "html.parser")
    html = html.find('main').select_one("div:nth-of-type(2)")
    planets = html.find_all('div', {'class': 'column is-one-third'})
    planet = random.choice(planets)
    number = planet.find('span').text
    name = planet.find('p', {'class': 'title'}).find('a').text
    url = f'{url}{name}'
    content = planet.find('div', {'class': 'content'}).find('p').text
    footer = planet.find('footer', {'class': 'card-footer'}).find_all('span')
    population = footer[0].text
    temperature = footer[1].text
    rarity = rarity_color(planet.find('div')['class'])
    return {'number': number, 'name': name, 'url': url, 'content': content, 'population': population, 'temperature': temperature, 'rarity': rarity}

def scrape_pixel_planet(planet):
    url = 'https://www.mypixelplanet.com/'
    response = requests.get(url+planet)
    if response.status_code == 404:
        return False
    html = BeautifulSoup(requests.get(url+planet).text, "html.parser")
    html = html.find('main').find('div')
    number = html.find('figure').find('span').text
    name = planet.capitalize()
    url = f'{url}{name}'
    content = next(html.find('h2').children).text
    footer = html.find('div').text
    footer = footer.replace('LIFEFORMS: ', '')
    footer = footer.split('TEMPERATURE: ')
    population = footer[0]
    temperature = footer[1]
    rarity = rarity_color(html.find('video')['class'])
    return {'number': number, 'name': name, 'url': url, 'content': content, 'population': population, 'temperature': temperature, 'rarity': rarity}

def scrape_depicted(depict):
    http = 'https://www.'
    site = 'thedepicted.com/'
    depict = depict.lower()
    html = BeautifulSoup(requests.get(http+site+depict).text, "html.parser")
    pictures = html.find('figure', {'class': 'image'}).find_all('picture')
    black = pictures[0].find('img')['src']
    color = pictures[1].find('img')['src']
    return {'http': http, 'site': site, 'depict': depict, 'black': (black, 0xFFFFFF), 'color': (color, 0x3273DC)}

def scrape_depicted_random():
    url = 'https://www.thedepicted.com/'
    page = random.choice(('', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'))
    html = BeautifulSoup(requests.get(url+page).text, "html.parser")
    depicts = html.find_all('div', {'class': 'column is-on-third-mobile is-two-thirds-tablet is-half-desktop is-one-third-widescreen is-one-quarter-fullhd'})
    depict = random.choice(depicts).find('a')['href']
    depict = depict[1:-1]
    return scrape_depicted(depict)

if __name__ == '__main__':
    scrape = scrape_pixel_planet("earth")
    print(scrape)
