import requests, json
from bs4 import BeautifulSoup
from pprint import pprint 
import re, pymysql
from song_info import get_songInfo
from album_info import get_albumInfo

url = "https://www.melon.com/chart/index.htm"

headers = {
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}


html = requests.get(url, headers=headers)
soup = BeautifulSoup(html.text, 'html.parser')
trs1 = soup.select('#lst50')
trs2 = soup.select('#lst100')



dic = {}
sinfodic = {}
ainfodic = {}

def get_list (trs) :
        
    for td in trs:
        
        dataSongNo = td.attrs['data-song-no']
        rank = td.select('td:nth-of-type(2) > div > span.rank')[0].text
        name = td.select('td:nth-of-type(6) > div > div > div.ellipsis.rank01 > span > a')[0].text
        artist = td.select('td:nth-of-type(6) > div > div > div.ellipsis.rank02 > a')
        artist = ", ".join([a.text for a in artist])
        likeCnt = ''

        href = td.select('td:nth-of-type(4) > div > a')[0].attrs['href']

        albumId = re.findall("\'(.*)\'", href)[0]

        tempDic = {'rank' : int(rank), "CONTSID": dataSongNo, "name": name , "artist" : artist, "likecnt" : likeCnt, 'albumId' : albumId}

        dic[dataSongNo] = tempDic


        songInfoDic = get_songInfo(dataSongNo)
       
        releaseDate = songInfoDic['releaseDate']
        album = songInfoDic['album']
        genre = songInfoDic['genre'] 

        stempDic = {'releaseDate' : releaseDate , "CONTSID": dataSongNo, "albumId": albumId, "album" : album, "genre" : genre, 'likecnt' : likeCnt, 'title' : name, 'singer' : artist}

        sinfodic[dataSongNo] = stempDic

        albumInfoDic =  get_albumInfo(albumId)

        albumlike = albumInfoDic['albumlike']
        agency = albumInfoDic['agency']
        rate = albumInfoDic['rate'] 
        albumtype = albumInfoDic['albumtype']

        atempDic = {'releaseDate' : releaseDate, "agency": agency, "albumId": albumId, "rate" : rate, 'albumlike' : albumlike, 'title' : name, 'albumtype' : albumtype, 'singer' : artist}

        ainfodic[albumId] = atempDic
    

get_list(trs1)
get_list(trs2)


jsonUrl = "https://www.melon.com/commonlike/getSongLike.json?"

jsonHeaders = { 'Referer': 'https://www.melon.com/chart/index.htm',
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}

jsonparams = { "contsIds" : ",".join(dic.keys()) }


jsonHtml = requests.get(jsonUrl, headers=jsonHeaders, params=jsonparams)
jsonData = json.loads(jsonHtml.text)

def set_likecnt(dic):
    for j in jsonData['contsLike']:
        songId = str(j['CONTSID'])
        x = dic.get(songId)
        if x == None :
            continue
        x['likecnt'] = j['SUMMCNT']

set_likecnt(dic)
set_likecnt(sinfodic)

dic = sorted(dic.items(), key=lambda d : d[1]['rank'])


# mysql에 데이터 넣기.
def get_mysql_conn(db):
    return pymysql.connect(
        host= '34.85.124.225',
        user='root',
        password='11',
        port=3306,
        db=db,
        charset='utf8')

# sql_truncate = "truncate table DailyList"
sql_dailyList = "insert into DailyList(rank, song_id, title, singer, likecnt, album_id) values(%s,%s,%s,%s,%s,%s)"
sql_songinfo = '''insert into SongInfo(song_id, album_name, album_id, genre, likecnt, release_date, singer, title) values(%s,%s,%s,%s,%s,%s,%s,%s)'''
sql_albuminfo = '''insert into AlbumInfo(release_date, agency, album_id, rate, album_likecnt, album_name, type, singer) values(%s,%s,%s,%s,%s,%s,%s,%s)'''


dailylistData =[]
songinfoData = []
albuminfoData = []

for row in dic:
        ll =[row[1]['rank'], row[1]['CONTSID'], row[1]['name'], row[1]['artist'], row[1]['likecnt'], row[1]['albumId'] ]
        dailylistData.append(ll)

for i in sinfodic.values():
        sl = [i['CONTSID'], i['album'], i['albumId'], i['genre'], i['likecnt'], i['releaseDate'], i['singer'], i['title']]
        songinfoData.append(sl)

for i in ainfodic.values():
        al = [ i['releaseDate'], i['agency'], i["albumId"], i["rate"], i['albumlike'],i['title'], i['albumtype'], i['singer'] ]
        albuminfoData.append(al)


conn = get_mysql_conn('hjdb')

with conn:
    cur = conn.cursor()
   
    cur.executemany(sql_songinfo, dailylistData)
    cur.executemany(sql_songinfo, songinfoData)
    cur.executemany(sql_albuminfo, albuminfoData)
       
    
    print("반영 된 수", cur.rowcount)