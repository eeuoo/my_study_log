import requests, json
from bs4 import BeautifulSoup
from pprint import pprint 
import re, pymysql


url = "http://vlg.berryservice.net:8099/melon/list"

html = requests.get(url)
soup = BeautifulSoup(html.text, 'html.parser')
trs1 = soup.select('#lst50')
trs2 = soup.select('#lst100')


singerList = []
sslist = []

def get_list (trs) :
        
    for td in trs:

        dataSongNo = td.attrs['data-song-no']

        name = td.select('td:nth-of-type(6) > div > div > div.ellipsis.rank01 > span > a')[0].text

        artists = td.select('td:nth-of-type(6) > div > div > div.ellipsis.rank02 > a')
        
        for singer in artists :
            sid = singer.attrs["href"]
            sid = re.findall("\'(.*)\'", sid)[0]
            al = (sid, singer.text)
            singerList.append(al)

            sl = (dataSongNo, name, singer.text, sid)
            sslist.append(sl)
    
get_list(trs1)
get_list(trs2)

singerList = list(set(singerList))

sslist = list(set(sslist))


sql_dupl_singer = "insert ignore into Singer(singer_id, singer_name) values(%s, %s)"

sql_dupl_ss = "insert ignore into MappingSongArtist (song_id, title, singer_name, singer_id) values(%s, %s, %s, %s)"

def get_mysql_conn(db):
    return pymysql.connect(
        host= '34.85.124.225',
        user='root',
        password='11',
        port=3306,
        db=db,
        charset='utf8')

conn = get_mysql_conn('hjdb')

with conn:
    cur = conn.cursor()

    cur.executemany(sql_dupl_singer, singerList)
    print("반영된 수", cur.rowcount)

    cur.executemany(sql_dupl_ss, sslist)
    print("반영된 수", cur.rowcount)

    

