
import requests, json
from bs4 import BeautifulSoup


def get_songInfo (songId) :
    
    url =' http://vlg.berryservice.net:8099/melon/songdetail?songId=' + str(songId)

    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    
    genre = soup.select_one( 'div.entry > div.meta > dl > dd:nth-of-type(3)').text
    releaseDate = soup.select_one('div.entry > div.meta > dl > dd:nth-of-type(2)').text.replace('.','')
    album = soup.select_one('div.entry > div.meta > dl > dd:nth-of-type(1) > a').text
    

    tempDic = {'releaseDate' : releaseDate , "CONTSID": '', "albumId": '' , "album" : album, "genre" : genre, 'likecnt' : '', 'title' : '', 'singer' : ''}

    return tempDic

