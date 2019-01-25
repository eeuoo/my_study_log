import requests, json
from bs4 import BeautifulSoup

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

