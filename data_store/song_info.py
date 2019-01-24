
import requests, json
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

