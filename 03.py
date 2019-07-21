import csv
import requests
from decouple import config
from datetime import datetime, timedelta
from pprint import pprint

key = config('API_KEY')
dict_result = {}
with open('movie.csv', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    name_list = []  
    movie_name = []
    for row in reader:
        name_list.append(row['peopleNm'])
        movie_name.append(row['movieNm'])
for i in range(len(name_list)):#len(name_list)
    url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleList.json?'
    url += f'key={key}&itemPerPage=100&peopleNm={name_list[i]}' 
    res = requests.get(url)
    dict_json = res.json()
    director_info = dict_json.get('peopleListResult').get('peopleList')
    for people in director_info:  ##딕셔너리 여러개가 들어가짐
        name = people.get('peopleNm')
        if name_list[i]==name and movie_name[i] in people.get('filmoNames'):
            if '감독' in people.get('repRoleNm'):
                dict_result [name] = {
                    'peopleCd' : people.get('peopleCd'),
                    'peopleNm' : people.get('peopleNm'),
                    'peopleNmEn' : people.get('peopleNmEn'),
                    'repRoleNm' : people.get('repRoleNm'),
                    'filmoNames' : people.get('filmoNames')
                }
                break
            else:
                dict_result [name] = {
                    'peopleCd' : people.get('peopleCd'),
                    'peopleNm' : people.get('peopleNm'),
                    'peopleNmEn' : people.get('peopleNmEn'),
                    'repRoleNm' : '정확한 내용이 아닙니다.',
                    'filmoNames' : people.get('filmoNames')
                }
                break

with open('director.csv', 'w', newline = '',encoding='utf-8') as f:
    fieldnames = ('peopleCd', 'peopleNm', 'peopleNmEn', 'repRoleNm', 'filmoNames') 
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for direct in dict_result.values():
        writer.writerow(direct)