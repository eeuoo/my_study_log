import requests, json
from bs4 import BeautifulSoup
import re

def get_albumInfo (albumId) :

    url = 'http://vlg.berryservice.net:8099/melon/detail?albumId=' + str(albumId)

    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')

    jsonUrl = "http://vlg.berryservice.net:8099/melon/albumlikejson?albumId=" + str(albumId)
    rateUrl = "http://vlg.berryservice.net:8099/melon/albumratejson?albumId=" + str(albumId)


    jsonHtml = requests.get(jsonUrl).text
    jsonData = json.loads(jsonHtml)

    rateHtml = requests.get(rateUrl).text
    rateData = json.loads(rateHtml)

    albumlike = jsonData['contsLike'][0]['SUMMCNT']
    rate = rateData["infoGrade"]["TOTAVRGSCORE"]
    agency = soup.select_one('div.entry > div.meta > dl > dd:nth-of-type(4)').text
    albumtype = soup.select_one('div.entry > div.info > span').text.strip()
    albumtype = re.findall("\[(.*)\]", albumtype)[0].strip()

    tempDic = {"agency": agency, "albumId": albumId, "rate" : rate, 'albumlike' : albumlike, 'albumtype' : albumtype}

    return tempDic

