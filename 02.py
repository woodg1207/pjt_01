import csv
import requests
from decouple import config
from datetime import datetime, timedelta
from pprint import pprint

key = config('API_KEY')
result = {}    

with open('boxoffice.csv', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    code_list = []  
    for row in reader:
        code_list.append(row['movieCd'])
for i in range(len(code_list)):  
    url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json?'
    url += f'key={key}&movieCd={int(code_list[i]) }'    ###int(code_list[i])       20192591
    res = requests.get(url)
    dict_json = res.json()
    movie_info = dict_json.get('movieInfoResult').get('movieInfo')
    
    for movie in movie_info:
        code = movie_info.get('movieCd')
        ####
        if movie_info.get('audits'):
            m = movie_info.get('audits')[0].get('watchGradeNm')
        else:
            m = '현재 정보가 없습니다.'
        if movie_info.get('directors'):
            n = movie_info.get('directors')[0].get('peopleNm')
        else:
            n = '현재 정보가 없습니다.'

        result[code] = {
            'movieCd' : movie_info.get('movieCd'),
            'movieNm' : movie_info.get('movieNm'),
            'movieNmEn' : movie_info.get('movieNmEn'),
            'movieNmOg' : movie_info.get('movieNmOg'),
            'watchGradeNm' : f'{m}' ,          
            'openDt' : movie_info.get('openDt')[:4],
            'showTm' : movie_info.get('showTm'),
            'genreNm' : movie_info.get('genres')[0].get('genreNm'),
            'peopleNm' : f'{n}'  
        }

with open('movie.csv', 'w', newline = '',encoding='utf-8') as f:
    #저장할 데이터들의 필드 이름을 미리 정한다. 
    fieldnames = ('movieCd', 'movieNm', 'movieNmEn', 'movieNmOg', 'watchGradeNm', 'openDt', 'showTm', 'genreNm', 'peopleNm') 
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    #필드 이름을 csv 파일 최상단에 작성한다.
    writer.writeheader()
    #딕셔너리를 순회하면 key를 통해 한줄씩 value를 작성한다.
    for moviechart in result.values():
        writer.writerow(moviechart)