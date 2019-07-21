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

- 01.py 를 제작하면서 50주간의 정보를 모으기 위해서 어떤 형식으로 작성해야하는게 더 쉬운 방법인지 고민을 했다. 이 과정에서 datetime이라는 형식을 배우게 되었고 50주간을 손쉽게 표현이 가능했다.
- 겹치는 영화코드 정보를 어떤 조건으로 처리해야하는지 고민을 했지만 풀수가 없었다. 결국 강사님의 도움을 통해서 코드를 작성할 수 있었다. 

### 2. 02.py 설명

- 01.py를 통해 얻은 대표코드를 boxoffice.csv에서 불러와 상세정보를 수집
- 영화 상세정보 API를 통해 영화 대표코드, 화명(국문), 화명(문), 화명(원문) ,관람등급, 개봉연도, 상시간, 장 르, 감독명 정보를 얻는다.
- 이후 movie.csv파일로 저장

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

- 01.py와 동일하게 key값을 config하여 보호하고 key 변수에 저장한다.
- boxoffice.csv파일을 열어 대표코드를 code_list내에 저장한다.

```python
for i in range(len(code_list)):
    url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json?'
    url += f'key={key}&movieCd={int(code_list[i]) }'   
    res = requests.get(url)
    dict_json = res.json()

    movie_info = dict_json.get('movieInfoResult').get('movieInfo')
```

- code_list의 길이 만큼 (대표코드의 수) 반복문을 수행하며 url을 요청한다
- 요청 받은 정보를 json형식으로 변화하고 movie_info 에 필요한 정보를 얻을수 있도록 접근후 저장한다.

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

- movie_info의 자료들중 빈 자료 일경우 오류가 나는것을 방지 하기위해서 조건문을 통해 자료가 있는경우에만 자료를 저장할 수 있도록 한다. 

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

- 조건문을 통해 정리된 자료와 그외의 자료들을 키값을 대표번호로 하고 벨류값이 딕셔너리 형식인 result 딕셔너리를 만든다. 

```python
with open('movie.csv', 'w', newline = '',encoding='utf-8') as f: 
    fieldnames = ('movieCd', 'movieNm', 'movieNmEn', 'movieNmOg', 'watchGradeNm', 'openDt', 'showTm', 'genreNm', 'peopleNm') 
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for moviechart in result.values():
        writer.writerow(moviechart)
```

- 생성한 result딕셔너리를 movie.csv에 쓰는 내용이다. 

#### 1-2 고찰

- 01.py를 수행 후 손쉽게 작성 할 수 있었다. 하지만 movie_info딕셔너리에서 필요한 정보로 가는중 아무 자료가 없는 경우가 있었다. 이때문에 에러가 발생했는데이를 해결하기위해 조건문을 통해 빈 값인경우 자료가 없다는것을 알리고 자료가 있는겨우에는 모든 자료를 보여주도록 작성했다.

### 3. 03.py 설명

- 영화인 정보 API를 사용한다. 이를 사용하기 위해 movie.csv에서 감독명과 영화제목을 갖고온다.
- 수집한 정보를 통해서 감독의 영화인 코드, 감독명, 분야, 필모리스트 정보를 구한다.
- 데이터들을 director.csv로 만든다.

#### 1-1 03.py code 설명

```python
key = config('API_KEY')
dict_result = {}
with open('movie.csv', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    name_list = []  
    movie_name = []
    for row in reader:
        name_list.append(row['peopleNm'])
        movie_name.append(row['movieNm'])
```

- movie.csv파일에서 감독명(peopleNm)과 영화이름(movieNm)정보를 갖고온 후 각각 name_list와 movie_name 변수에 저장한다.

```python
for i in range(len(name_list)):
    url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleList.json?'
    url += f'key={key}&itemPerPage=100&peopleNm={name_list[i]}' 
    res = requests.get(url)
    dict_json = res.json()
    director_info = dict_json.get('peopleListResult').get('peopleList')
```

- 전체를 name_list의 길이만큼 반복문을 수행하며 각각의 url들을 요청한다.
- 얻은 정보를 json형식으로 변환후 필요한 자료가 있는곳 까지 접근 후 director_info 에 넣는다.

```python
for people in director_info:  
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
```

- director_info를 반복문으로 돌리면서 조건문으로 movie.csv에서 갖고온 이름과 동일한 사람을 찾는다.
- 또한 동명이인의 경우를 줄이기 위해서 필모리스트와 영화의 이름을 비교하여 필모리스트에 영화제목이 있는겨우만을 찾도록 한다. 
- 조건문을 사요하여 '감독'이 포함되어있는지 확인한다. (조감독, 작화감독이 있는 경우를 대비)
- 또한 이외의 경우에는 정확한 내용이 아님을 표시해준다. 

```python
with open('director.csv', 'w', newline = '',encoding='utf-8') as f:
    fieldnames = ('peopleCd', 'peopleNm', 'peopleNmEn', 'repRoleNm', 'filmoNames') 
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for direct in dict_result.values():
        writer.writerow(direct)
```

- 최종적으로 정제된 dict_result를 director.csv파일로 쓰는 과정이다. 

#### 1-2 고찰

- 위의 두개의 코딩을 하면서 수월하게 작성을 할 수있었다. 
- 하지만 동명이인으로 인해 다른 영화인의 정보가 나오는 경우가 있었다. 이를 해결하기 위해서 여러 조건문을 만들기 위해 노력을 했지만 해당 영화제목이 필모리스트에 있다면 동명이인일 경우를 해결함을 알게 되었고 movie.csv파일에서 영화제목까지 갖고와 리스트로 만들었다.
- 또한 영화들중 감독이 아닌 조감독이 올라가 있는겨우가 었다. 그렇기 때문에 조건으로 감독을 포함하는 딕셔너리가 들어가도록 작성했다. 이외에도 직무가 아무것도 없는경우가 있었는데 이 경우에는 해당 자료가 정확하지 않음을 표기하도록 했다.

### 4. Python Code

#### 01.py code

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

#### 02.py code

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

#### 03.py code

```python
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
```