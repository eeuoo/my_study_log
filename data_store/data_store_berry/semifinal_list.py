import requests, json
from bs4 import BeautifulSoup
from pprint import pprint 
import re, pymysql
from song_info import get_songInfo
from album_info import get_albumInfo

url = "http://vlg.berryservice.net:8099/melon/list"

html = requests.get(url)
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

        atempDic = {'releaseDate' : releaseDate, "agency": agency, "albumId": albumId, 'album' : album, "rate" : rate, 'albumlike' : albumlike, 'albumtype' : albumtype, 'singer' : artist}

        ainfodic[albumId] = atempDic
    

get_list(trs1)
get_list(trs2)


jsonUrl = "http://vlg.berryservice.net:8099/melon/likejson"

jsonHtml = requests.get(jsonUrl)
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


sql_dailyList = "insert into DailyList(rank, song_id, title, singer, likecnt, album_id) values(%s,%s,%s,%s,%s,%s)"

sql_dupl_album = "insert into AlbumInfo(release_date, agency, album_id, album_name, rate, album_likecnt, type, singer) values(%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE release_date=release_date, agency=agency, album_id=album_id, album_name=album_name, type=type, singer=singer "

sql_dupl_song = "insert into SongInfo(song_id, title, album_name, album_id, genre, likecnt, release_date, singer) values(%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE song_id=song_id, title = title, album_name = album_name, album_id = album_id , genre =genre,release_date=release_date, singer=singer;"

dailylistData =[]
songinfoData = []
albuminfoData = []

for i in dic:
        i = i[1]
        ll =(i['rank'], i['CONTSID'], i['name'], i['artist'], i['likecnt'], i['albumId'] )
        dailylistData.append(ll)
        # print(dailylistData)

for i in sinfodic.values():
        sl = [i['CONTSID'], i['title'], i['album'], i['albumId'], i['genre'], i['likecnt'], i['releaseDate'], i['singer'] ]
        songinfoData.append(sl)

for i in ainfodic.values():
        al = [ i['releaseDate'], i['agency'], i["albumId"], i['album'], i["rate"], i['albumlike'], i['albumtype'], i['singer'] ]
        albuminfoData.append(al)

                
conn = get_mysql_conn('hjdb')

with conn:
    cur = conn.cursor()

    cur.executemany(sql_dupl_album, albuminfoData)
    print("반영 된 수", cur.rowcount)
    
    cur.executemany(sql_dupl_song, songinfoData)
    print("반영 된 수", cur.rowcount)

    for i in dailylistData:
        cur.execute(sql_dailyList, i)
    print("반영 된 수", cur.rowcount)
    