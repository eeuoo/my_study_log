import requests, json
from bs4 import BeautifulSoup
import re, pymysql

url = "https://openapi.naver.com/v1/search/blog.json"

title = "파이썬"
params = {
    "query": title,
    "display": 100,
    "start": 1,
    "sort": "date"
}

headers = {
    "X-Naver-Client-Id": "h8D7yhnqUBsVaCHQOViJ",
    "X-Naver-Client-Secret": "TYwzilDXGl"
}

result = requests.get(url, params=params, headers=headers).text

jsonData = json.loads(result)

# print(json.dumps(jsonData, ensure_ascii=False, indent=2))

Blog_list = []

for item in jsonData["items"]:

    title = item['title']
    bloggerName = item['bloggername']
    link = item['bloggerlink']
    postDate = item['postdate']

    title = title.replace('<b>','').replace('&lt;','<')
    title = title.replace('</b>','').replace('&gt;','> ')
    
    if 'blog.naver.com' in link:
        bloggerId = re.findall('.com/(.*)',link)[0]
    else : bloggerId = re.findall('.//(.*)/',link)[0]


    tempDic = { 'title' :  title, 'link' : link , 'bloggerId' : bloggerId, 'bloggerName' : bloggerName, 'postDate' : postDate }

    Blog_list.append(tempDic)


def get_mysql_conn(db):
    return pymysql.connect(
        host= 'localhost',
        user='doo',
        password='11',
        port=3306,
        db=db,
        charset='utf8')


blogger_ign_insert = "insert ignore into Blogger(id, blogger_name, link) values(%(bloggerId)s, %(bloggerName)s, %(link)s)"

blogPost_insert = "insert into BlogPost(id, title, addr, post_date) values(%(bloggerId)s, %(title)s, %(link)s, %(postDate)s)"

conn = get_mysql_conn('doodb')
with conn:
    cur = conn.cursor()

   
    cur.executemany(blogger_ign_insert, Blog_list)
    print("반영된 수", cur.rowcount)
    
    cur.executemany(blogPost_insert, Blog_list)
    print("반영된 수", cur.rowcount)


