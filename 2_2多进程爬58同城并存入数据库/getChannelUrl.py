#在http://nb.58.com中获取跳蚤市场频道的链接
from bs4 import BeautifulSoup
import requests
import pymongo

client = pymongo.MongoClient('localhost',27017)
tongcheng58 = client['tongcheng58']
channel_url = tongcheng58['channel_url']

start_url = 'http://nb.58.com'

webData = requests.get(start_url)
soup = BeautifulSoup(webData.text,'lxml')

for u in soup.select('div.fl.cbp2.cbhg > div:nth-of-type(1) em > a'):
    url = start_url + u.get('href')
    channel_url.insert_one({'url':url})
    print(url)