from bs4 import BeautifulSoup

html = '''
    <dl>
        <dt>국적</dt>
        <dd>대한민국</dd>

        <dt>활동장르</dt>
        <dd>Dance, Ballad, Drama</dd>
    
        <dt>데뷔</dt>
        <dd class="debut_song">
            <span class="ellipsis">
                2016.05.05
                <span class="bar">
                    TTT
                </span>
                <a href="#">TTTTTTTTTTTTT</a>
            </span>
        </dd>
        
        <dt>수상이력</dt>
        <dd class="awarded">
            <span class="ellipsis">
                2018 하이원 서울가요대상
                <span class="bar">|</span>본상
            </span>
        </dd>
    </dl>
'''

soup = BeautifulSoup(html, "html.parser")

cols = soup.select("dt")
rows = soup.select("dd")

keys = []
values = []

for a in cols :
    keys.append(a.text)

for i in rows:
    dd_span = i.find('span')
    dd_a = i.find('a')
    if dd_span != None and dd_a != None :
        j = dd_span.next.strip() 
        
    elif dd_span != None and dd_a == None :
        j = dd_span.next.strip() + dd_span.next.next.next.strip() + dd_span.next.next.next.next.strip()

    else :
        j = i.text
    
    values.append(j)



col_names = {}

for i in range(len(keys)):
    col_names[keys[i]] = values[i]


insert = "inset into Singer(nation, genre, debut, award) values('{}','{}','{}','{}')".format(col_names['국적'], col_names['활동장르'],col_names['데뷔'],col_names['수상이력'])

print(insert)