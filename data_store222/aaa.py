import requests, json, re
from bs4 import BeautifulSoup


def get_albumInfo (albumId) :

    url = 'http://vlg.berryservice.net:8099/melon/detail?albumId=' + str(albumId)


    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')
   

    jsonUrl = "http://vlg.berryservice.net:8099/melon/albumlikejson?albumId=" + str(albumId)
    rateUrl = "http://vlg.berryservice.net:8099/melon/albumratejson?albumId=" + str(albumId)


    jsonHtml = requests.get(jsonUrl).text
    rateHtml = requests.get(rateUrl).text
    

    jsonData = json.loads(jsonHtml)
    rateData = json.loads(rateHtml)
 
    albumlike = jsonData["contsLike"][0]['SUMMCNT']
    rate = rateData["infoGrade"]["TOTAVRGSCORE"]
    agency = soup.select_one('div.entry > div.meta > dl > dd:nth-of-type(4)').text
    albumtype = soup.select_one('div.entry > div.info > span').text.strip()
    albumtype = re.findall("\[(.*)\]", albumtype)[0].strip()

    tempDic = {"agency": agency, "albumId": albumId, "rate" : rate, 'albumlike' : albumlike, 'albumtype' : albumtype}

    return tempDic

a = get_albumInfo(10123639)
print(a)