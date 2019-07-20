[TOC]

# 파이썬을 활용한 데이터 수집1

## 프로젝트 요약

- 영화평점서비스를 제작하기 위한 데이터 수집 - Data Base구축을 위한 csv 활용
- 데이터 수집을 위한 영화진흥위원회 오픈 API 활용

### 1. 01.py 설명

- 영화진흥위원회의 오픈 API(주간/주말 박스오피스)를 사용
- 최근 50주간 데이터중 주간 박스오피스 TOP 10데이터를 수집

#### 1-1 01.py code 설명

```python
for i in range(50):
    key = config('API_KEY')
    targetDt = datetime(2019,7,13)-timedelta(weeks=i)
    targetDt = targetDt.strftime('%Y%m%d')
```

- 50주차를 알기위해서 50회 반복하는 반복문을 만들어준다.
- API를 사용하기 위해 필요한 key 값을 .env파일에 등록후 config를 사용하여 불러오도록 한다. (key값 보호)
- datetime을 활용하여 2019,07,13을 기준으로 50주 전까지의 날짜를 연산하고 targetDt 변수에 넣어준다. 
- .strftime()을 사용하여 필요한 데이터의 형식을 맞춰준다. ex) 20190713

```python
 url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.json?'
    url += f'itemPerPage=10&key={key}&'
    url += f'targetDt={targetDt}&weekGb=0&'
```

- 영화진흥위원회의 주간 박스오피스에 필요한 url을 갖고온다.
- 또한 f string을 사용하여 url주소에 key와 tagetDt변수를 넣어준다. 
- 주간 정보만을 얻기 위해서 weekGb=0으로 설정한다.

```python
res = requests.get(url)
    dict_json = res.json()
    m_list = dict_json.get('boxOfficeResult').get('weeklyBoxOfficeList')
```

- url을 통해서 얻은 정보를 requests를 사용하여 res 변수에 저장한다.
- res변수를 .json()을 사용하여 json 형식으로 변환한다.
- 요청한 정보는 딕셔너리 형식이기 때문에 필요로 하는 정보까지 .get()을 활용하여 접근 후 m_list 변수에 저장한다. 

```python
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
```

- 딕셔너리형식의 m_list를 반복하면서 movie에 넣어준다.
- code에 movieCd key의 value값을 넣어 각 영화별로 비교할 기준을 넣어 준다.
- 전체적인 반복문을 돌리면서 if 조건 문을 활용하여 code와 다른 영화 정보가 들어오면 result에 movieCd를 key값으로하고 value를 딕셔너리 형식으로 넣어준다.
- 처음의 result는 빈 딕셔너리 이다.
- 위의 for i in range(50): 은 이 코드 까지 반복한다.

```python
with open('boxoffice.csv', 'w', newline = '',encoding='utf-8') as f:
    #저장할 데이터들의 필드 이름을 미리 정한다. 
    fieldnames = ('movieCd', 'movieNm', 'audiAcc') 
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    #필드 이름을 csv 파일 최상단에 작성한다.
    writer.writeheader()
    #딕셔너리를 순회하면 key를 통해 한줄씩 value를 작성한다.
    for moviechart in result.values():
        writer.writerow(moviechart)
```

- boxoffice.csv를 만들어 주는 코드이다.
- 필드의 이름을 정해주고 반복문을 돌리면서 위의 result의 value값을 차례대로 작성하도록 만들어 준다.

#### 1-2 고찰

01.py 를 제작하면서 

#### 1-3 01.py code

```python
import requests
import csv
from decouple import config
from datetime import datetime, timedelta
from pprint import pprint

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
```



### 2. 02.py 설명

- 



#### 1-1 02.py code 설명

```python
key = config('API_KEY')
result = {}    

with open('boxoffice.csv', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    code_list = []  
    for row in reader:
        code_list.append(row['movieCd'])
```



```python
for i in range(186):
    url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json?'
    url += f'key={key}&movieCd={int(code_list[i]) }'   
    res = requests.get(url)
    dict_json = res.json()

    movie_info = dict_json.get('movieInfoResult').get('movieInfo')
```



```python
for movie in movie_info:
        code = movie_info.get('movieCd')
        if movie_info.get('audits'):
            m = movie_info.get('audits')[0].get('watchGradeNm')
        else:
            m = '현재 정보가 없습니다.'
        if movie_info.get('directors'):
            n = movie_info.get('directors')[0].get('peopleNm')
        else:
            n = '현재 정보가 없습니다.'
```



```python
 result[code] = {
            'movieCd' : movie_info.get('movieCd'),
            'movieNm' : movie_info.get('movieNm'),
            'movieNmEn' : movie_info.get('movieNmEn'),
            'movieNmOg' : movie_info.get('movieNmOg'),
            'watchGradeNm' : f'{m}' ,           ##빈값나올때?
            'openDt' : movie_info.get('openDt')[:4],
            'showTm' : movie_info.get('showTm'),
            'genreNm' : movie_info.get('genres')[0].get('genreNm'),
            'peopleNm' : f'{n}'  ##빈값나올때?
        }
```



```python
with open('movie.csv', 'w', newline = '',encoding='utf-8') as f: 
    fieldnames = ('movieCd', 'movieNm', 'movieNmEn', 'movieNmOg', 'watchGradeNm', 'openDt', 'showTm', 'genreNm', 'peopleNm') 
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for moviechart in result.values():
        writer.writerow(moviechart)
```



#### 1-2 고찰



```python
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
for i in range(186):
    url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json?'
    url += f'key={key}&movieCd={int(code_list[i]) }'   
    res = requests.get(url)
    dict_json = res.json()

    movie_info = dict_json.get('movieInfoResult').get('movieInfo')

    for movie in movie_info:
        code = movie_info.get('movieCd')
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
            'watchGradeNm' : f'{m}' ,           ##빈값나올때?
            'openDt' : movie_info.get('openDt')[:4],
            'showTm' : movie_info.get('showTm'),
            'genreNm' : movie_info.get('genres')[0].get('genreNm'),
            'peopleNm' : f'{n}'  ##빈값나올때?
        }
        
with open('movie.csv', 'w', newline = '',encoding='utf-8') as f: 
    fieldnames = ('movieCd', 'movieNm', 'movieNmEn', 'movieNmOg', 'watchGradeNm', 'openDt', 'showTm', 'genreNm', 'peopleNm') 
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for moviechart in result.values():
        writer.writerow(moviechart)
```







프로젝트 설명 요약 1~2줄

2. 01.py에 대한 설명 

-어떤 데이터를 가져와서 어떻게 저장했는지

-과정이나 시행착오를 적어서 

