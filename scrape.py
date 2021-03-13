import requests
import random
from bs4 import BeautifulSoup

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

    rarity_table = {
        'legendary': 0xFFDA87,
        'epic': 0x9400D3,
        'rare': 0x1E4ED1,
        'common': 0x6e7c7c,
    }
    rarity_classes = planet.find('div')['class']
    for rarity_class in rarity_classes:
        if rarity_class in rarity_table.keys():
            rarity = rarity_table[rarity_class]
        else:
            rarity = rarity_table['common']

    return (number, name, url, content, population, temperature, rarity)


if __name__ == '__main__':
    planet = scrape_pixel_random()
    print(planet)
