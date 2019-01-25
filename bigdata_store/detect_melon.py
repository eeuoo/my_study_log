import requests
import time

url = "https://www.melon.com/album/detail.htm?albumId=10218750"

heads = {
    "Referer": "https: // www.melon.com/chart/index.htm",
    "User-Agent": "Mozilla/5.0 (Macintosh Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
}

def beep():
    for i in range(10):
        print("\a")
        time.sleep(0.3)

while True:
    res = requests.get(url, headers=heads)
    print(res.status_code)
    if res.status_code != 406:
        print("OK", url)
        beep()
        break
    time.sleep(5)
