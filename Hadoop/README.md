![1](https://user-images.githubusercontent.com/44750085/53323802-85ebb880-3922-11e9-9c0a-3f57d37eacc7.png)

<br>

### 빅데이터 처리 기술이 출현하게 된 배경과 빅데이터 처리 시스템이 갖춰야 할 필수적인 기능이란.

빅데이터 처리 기술이 왜 출현하게 되었는지는 빅데이터를 보유하고 있는 기업들의 리스트만 봐도 감을 잡을 수 있다. 대표적인 빅데이터 보유 기업은 facebook, yahoo, twitter, ebay 등이 있다. 이전과 비교해 현대사회에서는 다양하고 많은 양의 데이터가 빠른 속도로 증가되고 있다. 흔히 규모, 속도, 다양성 3가지가 빅데이터의 3대 요소라고 불린다. 첫번째로 규모는, 비지니스 특성에 따라 다를 수 있지만 TB에서 PB 단위의 범위에 해당한다. 두번째 속도 역시 상황에 따라 다르다. 빅데이터를 장기적 접근할 수도 있겠지만, 데이터가 매우 빠른 속도로 생성되기 때문에 데이터의 생산, 저장, 수집, 분석도 실시간을 처리될 필요가 있다. 마지막으로 다양성은, 정형데이터부터 비정형데이터인 사진이나 영상까지 여러 형식의 데이터가 있다. 
방대한 양의 데이터가 저장되어 있더라고 그 데이터로 무언가 하지 않는 이상 쓸모가 없듯이, 빅데이터 처리 시스템은 거대해진 데이터를 저장하고 효율적으로 처리할 수 있는 기능이 필수적이다. TB와 PB 규모에 걸맞는 하드웨어와 소프트웨어 기술이 필요하며, 크고 다양한 데이터를 우리가 알아 볼 수 있는 데이터로 만드는 것이 핵심일 것이다. 

<br>
<br>


### 하둡(hadoop)의 핵심 기능인 HDFS와 MapReduce.

hdfs는 블록 구조의 파일 시스템으로, 데이터를 병렬적으로 저장할 수 있다.  hdfs에 저장하는 파일은 특정 사이즈의 블록으로 나줘져 분산된 서버에 저장된다. 블록 사이즈는 기본 64MB로, 변경이 가능하다. 기본적으로 네임 노드 서버 한 대, 데이터 노드 서버 여러 대로 구성된다. 데이터 노드는 주기적으로 네임 노드에게 하트비트와 블록의 목록이 저장된 블록 리포트를 보내준다. 네임 노드는 블록 리포트를 통해 모든 데이터 노드의 상황을 확인하고, 파일을 어느 곳에 줄 지 결정한다. 

하둡은 부산 파일 시스템인 hdfs에 데이터를 저장하고, 분산 처리 시스템인 mapreduce를 이용해 처리한다. 맵리듀스는 임의의 순서로 정렬된 데이터를 분산 처리(Map)하고 이를 다시 합치(Reduce)는 과정을 거친다. map은 key와 value 쌍으로 이뤄져 있고 reduce는 key를 기준으로 vlaue를 모두 더하거나, 평균을 내거나, 최대/최소를 구해 map을 정리해나간다.

YARN은 맵리듀스 프레임웍이외에도 다양한 종류의 분산처리환경을 지원합니다. yarn의  Resource Manager 클러스터마다 존재하며, 클러스터 전반의 자원 관리와 스케쥴링을 담당한다  클라이언트로부터 애플리케이션 실행 요청을 받으면 그 애플리케이션의 실행을 책임질 Application Master를 실행한다. 또한 클러스터 내에 설치된 모든 Node Manager와 통신을 통해서 각 서버마다 할당된 자원과 사용중인 자원의 상황을 알 수 있으며, Application Master들과의 통신을 통해 필요한 자원이 무엇인지 알아내어 관리하게 된다.

<br>
<br>


### sample data를 이용하여 연간 최고 기온 구하는 map과 reduce 함수 코딩하기.
```python

from pprint import pprint
import sys

sample_data = '''0067011990999991950051507004+68750+023550FM-12+038299999V0203301N00671220001CN9999999N9+00001+99999999999
0043011990999991945051512004+68750+023550FM-12+038299999V0203201N00671220001CN9999999N9+00225+99999999999
0043011990999991950051518004+68750+023550FM-12+038299999V0203201N00261220001CN9999999N9-00111+99999999999
0043012650999991949032412004+62300+010750FM-12+048599999V0202701N00461220001CN0500001N9+01117+99999999999
0043012650999991943032418004+62300+010750FM-12+048599999V0202701N00461220001CN0500001N9+00384+99999999999
0043012650999991945032412004+62300+010750FM-12+048599999V0202701N00461220001CN0500001N9+00167+99999999999
0043012650999991947032412004+62300+010750FM-12+048599999V0202701N00461220001CN0500001N9-00150+99999999999
0043012650999991949032412004+62300+010750FM-12+048599999V0202701N00461220001CN0500001N9+00117+99999999999
0043012650999991947032412004+62300+010750FM-12+048599999V0202701N00461220001CN0500001N9+00227+99999999999
0043012650999991945032412004+62300+010750FM-12+048599999V0202701N00461220001CN0500001N9+01116+99999999999
0043012650999991943032412004+62300+010750FM-12+048599999V0202701N00461220001CN0500001N9-00114+99999999999
0043012650999991943032412004+62300+010750FM-12+048599999V0202701N00461220001CN0500001N9+00191+99999999999
0043012650999991949032412004+62300+010750FM-12+048599999V0202701N00461220001CN0500001N9+00131+99999999999'''

data = sample_data.split('\n')

a = [0,1,4,5,9]

def map():
    for i in data:
        (year, temp) = i[15:19],i[-18:-12]

        if int(temp[-1]) in a :
            t = temp[:-1]
            i = (year, int(t))

            yield i
        

def reduce(m):
    dic = {}

    for tupl in m :
        (key, value) =  tupl
        try:
            if dic[key] < value:
                dic[key] = value
        except KeyError :
            dic[key] = value

    return dic


result = reduce(map())
pprint(result)
        



# 자리수: 년도, 온도, 구분값(0,1,4,5,9만 해당됨)
```


<br>
<br>
<br>


### 빅데이터 수집 시 적재된 Song 테이블과 Album 테이블의 모든 데이터를 BigQuery로 저장하고, 노래 정보에 앨범명까지 출력하기.
```python

import pymysql, sys
import bigquery


def get_conn(db):
  return pymysql.connect( 
        host = '34.85.124.225',
        user = 'root',
        password = '비밀번호' ,
        port = 3306 ,
        db = db ,
        charset = 'utf8' )


def get_songs():

    conn = get_conn('hjdb')

    with conn:
        cur = conn.cursor()
        select_query = "select s.*, a.rate as album_rate, a.album_likecnt as album_likecnt, a.type as type, a.agency as agency from SongInfo s inner join AlbumInfo a on s.album_id = a.album_id"
        cur.execute(select_query)
        
        Songs = cur.fetchall()
        columns = cur.description 

        result = [{columns[index][0]:column for index, column in enumerate(value)} for value in Songs] 

        rr = [ {'song_id' : dic['song_id'], 
                'likecnt' : dic['likecnt'], 
                'title' : dic['title'],
                'genre' : dic['genre'],
                'singer' : dic['singer'],
                'release_date': dic['release_date'],
                'album' : {'album_id' : dic['album_id'],
                            'album_name': dic['album_name'],
                            'album_rate': float(dic['album_rate']),
                            'album_likecnt': dic['album_likecnt'],
                            'type': dic['type'],
                            'agency' : dic['agency']
                          }
                } for dic in result ]

        return rr

DATABASE = "bqdb"
TABLE = "Song"

client = bigquery.get_client(json_key_file='./bigquery.json', readonly=False)

if not client.check_table(DATABASE, TABLE):
    print("Create table {0}.{1}".format(DATABASE, TABLE), file=sys.stderr)

    client.create_table(DATABASE, TABLE, [
        {'name': 'song_id', 'type': 'string', 'description': 'song id'},
        {'name': 'title', 'type': 'string', 'description': 'song title'},
        {'name': 'singer', 'type': 'string', 'description': 'singer'},
        {'name': 'release_date', 'type': 'string', 'description': 'release date'},
        {'name': 'likecnt', 'type': 'string', 'description': 'song like count'},
        {'name': 'genre', 'type': 'string', 'description': 'song genre'},
        {'name': 'album', 'type': 'RECORD', 'description':'album information', 'fields' : [
                    {'name': 'album_name', 'type': 'string', 'description': 'album title'},
                    {'name': 'album_likecnt', 'type': 'string', 'description': 'album like count'},
                    {'name': 'album_rate', 'type': 'FLOAT', 'description': 'album rate'},
                    {'name': 'album_id', 'type': 'string', 'description': 'album id'},
                    {'name': 'agency', 'type': 'string', 'description': 'agency'},
                    {'name': 'type', 'type': 'string', 'description': 'album type'}
                    ] }
        ]
    )

ttt = get_songs()

pushResult = client.push_rows(DATABASE, TABLE, ttt, insert_id_key='songno')
print("Pushed Result is", pushResult)

```
```python
from google.cloud import bigquery as bigq
from pprint import pprint

client2 = bigq.Client()

QUERY = ('SELECT song_id, title, singer, release_date, likecnt, genre, album.album_name FROM `precise-passkey-221515.bqdb.Song` LIMIT 1000')

query_job = client2.query(QUERY)
rows = query_job.result()

for row in rows:
    print(row)
```



