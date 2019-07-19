import requests
import csv
from decouple import config
from datetime import datetime, timedelta
from pprint import pprint

# datetime(2017,7,13)-timedelta(weeks=i)
#.strftime('%Y%m%d')

result = {}

for i in range(50):
    key = config('API_KEY')
    targetDt = datetime(2019,7,13)-timedelta(weeks=i)
    targetDt = targetDt.strftime('%Y%m%d')

    
    url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.json?'
    url += f'itemPerPage=10&key={key}&'
    url += f'targetDt={targetDt}&weekGb=0&'

    res = requests.get(url)
    dict_json = res.json()
    m_list = dict_json.get('boxOfficeResult').get('weeklyBoxOfficeList')
    for movie in m_list:
        code = movie.get('movieCd')
        if code not in result:##날짜를 거꾸로 돌아가면서 데이터를 얻기 때문에 
            #기존에 이미 영화코드가 들어가 있다면,
            #그게 가장 마지막 주 데이터다. 즉 기존 영화코드가 있다면 딕셔너리에 넣지 않는다
            result[code] = {
                'movieCd' : movie.get('movieCd'),
                'movieNm' : movie.get('movieNm'),
                'audiAcc' : movie.get('audiAcc'),
            }

        

with open('boxoffice.csv', 'w', newline = '',encoding='utf-8') as f:
    #저장할 데이터들의 필드 이름을 미리 정한다. 
    fieldnames = ('movieCd', 'movieNm', 'audiAcc') 
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    #필드 이름을 csv 파일 최상단에 작성한다.
    writer.writeheader()
    #딕셔너리를 순회하면 key를 통해 한줄씩 value를 작성한다.
    for moviechart in result.values():
        writer.writerow(moviechart)

