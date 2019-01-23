
import requests, json
from bs4 import BeautifulSoup


def get_songInfo (songId) :
    
    url = 'https://www.melon.com/song/detail.htm?songId=' + str(songId)

    headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }

    html = requests.get(url, headers=headers)
    soup = BeautifulSoup(html.text, 'html.parser')

    genre = soup.select_one( 'div.entry > div.meta > dl > dd:nth-child(6)').text
    releaseDate = soup.select_one('div.entry > div.meta > dl > dd:nth-child(4)').text.replace('.','')
    album = soup.select_one('div.entry > div.meta > dl > dd:nth-child(2) > a').text
    

    tempDic = {'releaseDate' : releaseDate , "CONTSID": '', "albumId": '' , "album" : album, "genre" : genre, 'likecnt' : '', 'title' : '', 'singer' : ''}

    return tempDic

