import requests
from bs4 import BeautifulSoup
import lxml
import json
from time import sleep


# list_person_hrefs = []
# for i in range(0, 740, 20):
#     url = f"https://www.bundestag.de/ajax/filterlist/en/members/863330-863330?limit=20&noFilterSet=true&offset={i}"
#
#     q = requests.get(url)
#     result = q.content
#
#     soup = BeautifulSoup(result, "lxml")
#
#     div_persons = soup.find_all("div", {"class": "col-xs-4 col-sm-3 col-md-2 bt-slide"})
#
#     for div_person in div_persons:
#         person_href = div_person.find("a").get("href")
#         list_person_hrefs.append(person_href)
#
# with open("list_person_hrefs.txt", "w", encoding="utf-8") as file:
#     for line in list_person_hrefs:
#         file.write(f"{line}\n")

persons_hrefs_list = []
count = 1
with open("list_person_hrefs.txt", encoding="utf-8") as file:
    for line in file.readlines():
        persons_hrefs_list.append(line.strip())

data_list = []

count = 1
for href in persons_hrefs_list:
    q = requests.get(href)

    result = q.content

    soup = BeautifulSoup(result, "lxml")

    person_name_part = soup.find("div", {"class": "col-xs-8 col-md-9 bt-biografie-name"}).find("h3").text.strip()
    person_name_part_list = person_name_part.split(",")
    person_name = person_name_part_list[0].strip()
    person_part = person_name_part_list[1].strip()



    links_list_social = soup.find_all("a", class_="bt-link-extern")

    social_networks = {}
    for link in links_list_social:
        name_social = link.get("title").strip()
        href_social = link.get("href").strip()

        social_networks[name_social] = href_social

    data = {
        "person_name": person_name,
        "person_company": person_part,
        "social_networks": social_networks
    }

    data_list.append(data)

    print(f"Всего выполнено: {count}\n{person_name} добавлен")

    if count % 30 == 0:
        sleep(6)
        
    count += 1

    with open("persons_data.json", "w", encoding="utf-8") as file:
        json.dump(data_list, file, indent=4, ensure_ascii=False)

