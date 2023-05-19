import requests
from fake_headers import Headers
from pprint import pprint
from bs4 import BeautifulSoup

parsed_data = []
def get_headers():
    return Headers(browser='firefox', os='win').generate()

source_for_parsing = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'
moscow_spb = {
    'text': 'python',
    'area1': '1',
    'area2': '2'
}

vacansies = requests.get(source_for_parsing, headers=get_headers(), params=moscow_spb).text
hh_main_soup = BeautifulSoup(vacansies, 'lxml')
tag_all_vacansies = hh_main_soup.find('div', class_="HH-MainContent HH-Supernova-MainContent")
vacancy_tag = tag_all_vacansies.find_all('div', class_="vacancy-serp-item-body__main-info")

for vacancy in vacancy_tag:
    link = vacancy.find('a')['href']
    # tag_h3 = vacancy[3].find('h3')
    # tag_a = tag_h3.find('tag_a')
    # link = tag_a['href']
    vacancy_page = BeautifulSoup(requests.get(link, headers=get_headers()).text, 'lxml')
    vacancy_description = vacancy_page.find('div', class_="vacancy-description").text

    if 'Django' and 'Flask' in vacancy_description:
        salary = vacancy_page.find('div', class_="vacancy-title").find_all('div')[1].text
        company = vacancy_page.find('span', class_="vacancy-company-name").text
        city = vacancy_page.find('span', {'data-qa': 'vacancy-view-raw-address'}).contents[0]
        parsed_data.append(
            {
                'link': link,
                'company': company,
                'city': city,
                'salary': salary
            }
        )

pprint(parsed_data)