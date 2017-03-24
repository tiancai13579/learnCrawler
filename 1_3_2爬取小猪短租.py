from bs4 import BeautifulSoup
import requests
import time

info = []
url1 = 'http://hz.xiaozhu.com/fangzi/6984584416.html'
url2 = 'http://hz.xiaozhu.com/fangzi/6007555016.html'
url3 = 'http://hz.xiaozhu.com/fangzi/6901066716.html'
urls = ['http://hz.xiaozhu.com/search-duanzufang-p{}-0/'.format(str(i)) for i in range(1,7)]
url = 'http://hz.xiaozhu.com/search-duanzufang-p5-0/'
headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
}

#获取详情页信息
def getInfo(url):
    web_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(web_data.text,'lxml')
    #print(soup)
    title = soup.select('div.pho_info > h4 > em')[0].text
    position = soup.select('div.pho_info > p > span')[0].text.strip()#最后一个函数剔除空格
    price = soup.select('#pricePart > div.day_l > span')[0].text
    house_pic = soup.select('#curBigImage')[0].get('src')
    owner_name = soup.select('a.lorder_name')[0].get('title')
    owner_pic = soup.select('#floatRightBox > div.js_box.clearfix > div.member_pic > a > img')[0].get('src')
    owner_sex = soup.select('div.member_pic > div')[0].get('class')[0]
    if owner_sex == 'member_ico1':
        owner_sex = '女'
    else:
        owner_sex = '男'
    #print(title,position,price,house_pic,owner_name,owner_pic,owner_sex,sep='\n-----------------\n')
    data = {
        'title':title,
        'position':position,
        'price':price,
        'house_pic':house_pic,
        'owner_name':owner_name,
        'owner_pic':owner_pic,
        'owner_sex':owner_sex
    }
    print(data)
    info.append(data)

#导航页获取详情页url
def startPage(url):
    web_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(web_data.text, 'lxml')
    urls = soup.select('#page_list > ul > li > a')
    #print(urls)
    for u in urls:
        getInfo(u.get('href'))

#getInfo(url1)
#getInfo(url2)
#getInfo(url3)
for u in urls:
    startPage(url)