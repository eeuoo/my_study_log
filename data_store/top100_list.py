import requests, json
from bs4 import BeautifulSoup
from pprint import pprint 
import re
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
       
        songInfoDic['CONTSID'] = dataSongNo
        songInfoDic['albumId'] = albumId
        songInfoDic['likecnt'] = likeCnt
        songInfoDic['title'] = name
        songInfoDic['singer'] = artist

        sinfodic[dataSongNo] = songInfoDic

        albumInfoDic =  get_albumInfo(albumId)

        albumInfoDic['title'] = name
        albumInfoDic['singer'] = artist
        albumInfoDic['releaseDate'] = songInfoDic['releaseDate']

        ainfodic[albumId] = albumInfoDic 
    

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

pprint(dic)