## Melon Top100 크롤하여 MySQL에 저장하기

### Crawl, Migration, Store   - Python
* melon top 100 페이지에서 유의미한 데이터를 크롤한다.
* 유의미한 데이터는 top100 리스트, 노래 상세 정보, 앨범 상세 정보, 가수 등으로 구성하였다.

```python
# main

import requests, json, re, pymysql
from bs4 import BeautifulSoup

from song_info import get_songInfo
from album_info import get_albumInfo
from get_songlike import get_songLike

url = "https://www.melon.com/chart/index.htm"

headers = {
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}


html = requests.get(url, headers=headers)
soup = BeautifulSoup(html.text, 'html.parser')
trs1 = soup.select('#lst50')
trs2 = soup.select('#lst100')


top100list = []
songinfolist = []
albuminfolist = []
singerList = []
sslist = []

def get_list (trs) :
        
    for td in trs:
        
        # Top100 구성
        dataSongNo = td.attrs['data-song-no']
        rank = td.select('td:nth-of-type(2) > div > span.rank')[0].text
        name = td.select('td:nth-of-type(6) > div > div > div.ellipsis.rank01 > span > a')[0].text
        artists = td.select('td:nth-of-type(6) > div > div > div.ellipsis.rank02 > a')
        artist = ", ".join([a.text for a in artists])
        likeCnt = get_songLike(dataSongNo)

        href = td.select('td:nth-of-type(4) > div > a')[0].attrs['href']
        albumId = re.findall("\'(.*)\'", href)[0]

        top100 = (int(rank), dataSongNo, name , artist, likeCnt, albumId)
        top100list.append(top100)

        # 노래 상세 정보 구성
        songInfoDic = get_songInfo(dataSongNo)
       
        releaseDate = songInfoDic['releaseDate']
        album = songInfoDic['album']
        genre = songInfoDic['genre'] 

        songinfos = (releaseDate , dataSongNo, albumId, album, genre, likeCnt, name, artist)
        songinfolist.append(songinfos)

        # 앨범 상세 정보 구성
        albumInfoDic =  get_albumInfo(albumId)

        albumlike = albumInfoDic['albumlike']
        agency = albumInfoDic['agency']
        rate = albumInfoDic['rate'] 
        albumtype = albumInfoDic['albumtype']

        albuminfos = (releaseDate, agency, albumId, album, rate, albumlike, albumtype, artist)
        albuminfolist.append(albuminfos)
        
        # 가수, 매핑(가수-노래) 구성
        for singer in artists :
            sid = singer.attrs["href"]
            sid = re.findall("\'(.*)\'", sid)[0]
            
            al = (sid, singer.text)
            singerList.append(al)

            sl = (dataSongNo, name, singer.text, sid)
            sslist.append(sl)
    

get_list(trs1)
get_list(trs2)

albuminfolist = (list(set(albuminfolist)))
singerList = list(set(singerList))
sslist = list(set(sslist))


# mysql에 데이터 넣기.
def get_mysql_conn(db):
    return pymysql.connect(
        host= '34.85.124.225',
        user='root',
        password='11',
        port=3306,
        db=db,
        charset='utf8')


sql_dailyList = "insert into DailyList(rank, song_id, title, singer, likecnt, album_id) values(%s,%s,%s,%s,%s,%s)"

sql_dupl_album = "insert into AlbumInfo(release_date, agency, album_id, album_name, rate, album_likecnt, type, singer) values(%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE release_date=release_date, agency=agency, album_id=album_id, album_name=album_name, type=type, singer=singer "

sql_dupl_song = "insert into SongInfo(release_date, song_id, album_id, album_name, genre, likecnt, title, singer) values(%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE song_id=song_id, title = title, album_name = album_name, album_id = album_id , genre =genre,release_date=release_date, singer=singer;"

sql_dupl_singer = "insert ignore into Singer(singer_id, singer_name) values(%s, %s)"

sql_dupl_ss = "insert ignore into MappingSongArtist (song_id, title, singer_name, singer_id) values(%s, %s, %s, %s)"

conn = get_mysql_conn('hjdb')

with conn:
    cur = conn.cursor()

    cur.executemany(sql_dupl_album, albuminfolist)
    print("반영된 수", cur.rowcount)

    cur.executemany(sql_dupl_song, songinfolist)
    print("반영된 수", cur.rowcount)
   
    cur.executemany(sql_dailyList, top100list)
    print("반영된 수", cur.rowcount)
    
    cur.executemany(sql_dupl_singer, singerList)
    print("반영된 수", cur.rowcount)

    cur.executemany(sql_dupl_ss, sslist)
    print("반영된 수", cur.rowcount)

```
```python
# utils

import requests, json, re
from bs4 import BeautifulSoup


def get_songInfo (songId) :
    
    url = 'https://www.melon.com/song/detail.htm?songId=' + str(songId)

    headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }

    html = requests.get(url, headers=headers)
    soup = BeautifulSoup(html.text, 'html.parser')
    
    genre = soup.select_one( 'div.entry > div.meta > dl > dd:nth-of-type(3)').text
    releaseDate = soup.select_one('div.entry > div.meta > dl > dd:nth-of-type(2)').text.replace('.','')
    album = soup.select_one('div.entry > div.meta > dl > dd:nth-of-type(1) > a').text
    

    tempDic = {'releaseDate' : releaseDate, "album" : album, "genre" : genre }

    return tempDic




def get_songLike(songid) :

    jsonUrl = "https://www.melon.com/commonlike/getSongLike.json?"

    jsonHeaders = { 'Referer': 'https://www.melon.com/chart/index.htm',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }

    jsonparams = { "contsIds" : songid }


    jsonHtml = requests.get(jsonUrl, headers=jsonHeaders, params=jsonparams)
    jsonData = json.loads(jsonHtml.text)

    
    likecnt = jsonData['contsLike'][0]['SUMMCNT']

    return likecnt



def get_albumInfo (albumId) :

    url = 'https://www.melon.com/album/detail.htm?albumId=' + str(albumId)


    headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }


    html = requests.get(url, headers=headers)
    soup = BeautifulSoup(html.text, 'html.parser')

    jsonUrl = "https://www.melon.com/commonlike/getAlbumLike.json?"
    rateUrl = "https://www.melon.com/album/albumGradeInfo.json?"

    jsonHeaders = { 'Referer': url,
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }

    jsonparams = { "contsIds" : str(albumId) }
    rateparams = {'albumId' : str(albumId)}

    jsonHtml = requests.get(jsonUrl, headers=jsonHeaders, params=jsonparams)
    jsonData = json.loads(jsonHtml.text)

    rateHtml = requests.get(rateUrl, headers=jsonHeaders, params=rateparams)
    rateData = json.loads(rateHtml.text)

    albumlike = jsonData['contsLike'][0]['SUMMCNT']
    rate = rateData["infoGrade"]["TOTAVRGSCORE"]
    agency = soup.select_one('div.entry > div.meta > dl > dd:nth-of-type(4)').text
    albumtype = soup.select_one('div.entry > div.info > span').text.strip()
    albumtype = re.findall("\[(.*)\]", albumtype)[0].strip()

    tempDic = {"agency": agency, "albumId": albumId, "rate" : rate, 'albumlike' : albumlike, 'albumtype' : albumtype}

    return tempDic

```

### Create Table - MySQL
* 크롤한 데이터 간 관계성을 맺고, 데이터 분석에 활용한다.
* show create table로 가져온 것이므로 fk가 테이블 생성 쿼리 안에 있지만, 실제로는 alter로 구성하였음.
```sql
drop table if exists AlbumInfo;
CREATE TABLE `AlbumInfo` (
  `album_id` int(11) NOT NULL,
  `album_name` varchar(256) DEFAULT NULL,
  `agency` varchar(256) DEFAULT NULL,
  `rate` decimal(4,1) DEFAULT NULL,
  `album_likecnt` int(11) DEFAULT NULL,
  `type` varchar(8) DEFAULT NULL,
  `singer` varchar(512) DEFAULT NULL,
  `release_date` varchar(31) DEFAULT NULL,
  PRIMARY KEY (`album_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

drop table if exists SongInfo;
CREATE TABLE `SongInfo` (
  `song_id` int(11) NOT NULL,
  `title` varchar(128) DEFAULT NULL,
  `genre` varchar(50) DEFAULT NULL,
  `singer` varchar(512) DEFAULT NULL,
  `likecnt` int(11) DEFAULT NULL,
  `album_id` int(11) NOT NULL,
  `album_name` varchar(256) DEFAULT NULL,
  `release_date` varchar(31) DEFAULT NULL,
  PRIMARY KEY (`song_id`),
  KEY `fk_albumid_idx` (`album_id`),
  CONSTRAINT `fk_albumid` FOREIGN KEY (`album_id`) REFERENCES `AlbumInfo` (`album_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

drop table if exists DailyList;
CREATE TABLE `DailyList` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `rank` smallint(6) NOT NULL,
  `title` varchar(128) DEFAULT NULL,
  `singer` varchar(512) DEFAULT NULL,
  `likecnt` int(11) DEFAULT NULL,
  `song_id` int(11) NOT NULL,
  `album_id` int(11) NOT NULL,
  `crawl_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_daily_songid_idx` (`song_id`),
  KEY `fk_album_idx` (`album_id`)
) ENGINE=InnoDB AUTO_INCREMENT=901 DEFAULT CHARSET=utf8;

drop table if exists Singer;
CREATE TABLE `Singer` (
  `singer_id` int(11) NOT NULL,
  `singer_name` varchar(126) DEFAULT NULL,
  PRIMARY KEY (`singer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

drop table if exists MappingSS;
CREATE TABLE `MappingSS` (
  `song_id` int(11) NOT NULL,
  `title` varchar(128) DEFAULT NULL,
  `singer_name` varchar(126) DEFAULT NULL,
  `singer_id` int(11) NOT NULL,
  PRIMARY KEY (`song_id`,`singer_id`),
  KEY `fk_singerid_idx` (`singer_id`),
  CONSTRAINT `fk_singerid` FOREIGN KEY (`singer_id`) REFERENCES `Singer` (`singer_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_songid` FOREIGN KEY (`song_id`) REFERENCES `SongInfo` (`song_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

```


