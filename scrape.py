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
    # image = planet.find('img')['src']
    name = planet.find('p', {'class': 'title'}).find('a').text
    image = f'{url}{name}.gif'
    content = planet.find('div', {'class': 'content'}).find('p').text
    footer = planet.find('footer', {'class': 'card-footer'}).find_all('span')
    population = footer[0].text
    temperature = footer[1].text
    return (number, name, image, content, population, temperature)


if __name__ == '__main__':
    scrape_pixel_random()
