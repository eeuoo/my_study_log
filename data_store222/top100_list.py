import requests, json
from bs4 import BeautifulSoup
from pprint import pprint 
import re
from song_info import get_songInfo
from album_info import get_albumInfo
import csv, codecs


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
        rank = td.select('td:nth-child(2) > div > span.rank')[0].text
        name = td.select('td:nth-child(6) > div > div > div.ellipsis.rank01 > span > a')[0].text
        artist = td.select('td:nth-child(6) > div > div > div.ellipsis.rank02 > a')
        artist = ", ".join([a.text for a in artist])
        likeCnt = ''

        href = td.select('td:nth-child(4) > div > a')[0].attrs['href']

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


with codecs.open('./melon_dailyList.csv', 'w', encoding='utf-8') as ff:
    writer = csv.writer(ff, delimiter=',', quotechar='"')

    writer.writerow(['랭킹', '곡 id', '곡명', '가수', '좋아요수','앨범id'])

    for row in dic:
        writer.writerow([row[1]['rank'], row[1]['CONTSID'], row[1]['name'], row[1]['artist'], row[1]['likecnt'], row[1]['albumId'] ])
        
   
with codecs.open('./melon_songinfo.csv', 'w', encoding='utf-8') as ff:
        writer = csv.writer(ff, delimiter=',', quotechar='"')

        writer.writerow(['곡 id', '곡명', '앨범명', '앨범id', '장르', '좋아요수','발매일','가수'])

        for i in sinfodic.values():
               writer.writerow([i['CONTSID'], i['title'], i['album'], i['albumId'], i['genre'], i['likecnt'], i['releaseDate'], i['singer'] ])


with codecs.open('./melon_albuminfo.csv', 'w', encoding='utf-8') as ff:
        writer = csv.writer(ff, delimiter=',', quotechar='"')

        writer.writerow(['발매일', '기획사', '앨범id','앨범', '평점', '좋아요수', '앨범 타입', '가수'])

        for i in ainfodic.values():
                writer.writerow([ i['releaseDate'], i['agency'], i["albumId"], i['album'], i["rate"], i['albumlike'], i['albumtype'], i['singer'] ])
        