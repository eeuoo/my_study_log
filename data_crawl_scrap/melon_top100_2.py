import requests, json
from bs4 import BeautifulSoup
from pprint import pprint 

url = "https://www.melon.com/chart/index.htm"

headers = {
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}


html = requests.get(url, headers=headers)
soup = BeautifulSoup(html.text, 'html.parser')
trs1 = soup.select('#lst50')
trs2 = soup.select('#lst100')


dic = {}

def get_list (trs) :
        
    for td in trs:
        
        dataSongNo = td.attrs['data-song-no']
        rank = td.select('td:nth-child(2) > div > span.rank')[0].text
        name = td.select('td:nth-child(6) > div > div > div.ellipsis.rank01 > span > a')[0].text
        artist = td.select('td:nth-child(6) > div > div > div.ellipsis.rank02 > a')
        likeCnt = ''

        if len(artist) > 2 :
            artistList = []
            for i in artist :
                artistList.append(i.text)
            artist = artistList
        else : artist = artist[0].text

        tempDic = {'rank' : int(rank), "CONTSID": dataSongNo, "name": name , "artist" : artist, "likeCnt" : likeCnt}

        dic[dataSongNo] = tempDic

get_list(trs1)
get_list(trs2)



jsonUrl = "https://www.melon.com/commonlike/getSongLike.json?"

jsonHeaders = { 'Referer': 'https://www.melon.com/chart/index.htm',
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}

jsonparams = { "contsIds" : ",".join(dic.keys()) }


jsonHtml = requests.get(jsonUrl, headers=jsonHeaders, params=jsonparams)
jsonData = json.loads(jsonHtml.text)
# songInfo = json.dumps(jsonData, ensure_ascii=False, indent=2)


for j in jsonData['contsLike']:
    songId = str(j['CONTSID'])
    x = dic.get(songId)
    if x == None :
        continue
    x['likeCnt'] = j['SUMMCNT']


dic = sorted(dic.items(), key=lambda d : d[1]['rank'])

pprint(dic)


# for i in dic.values() :
#     print("{}위 {} - {}  ♡ {}".format(i['rank'], i['name'], i['artist'], i['likeCnt']))