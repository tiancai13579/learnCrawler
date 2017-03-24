from bs4 import BeautifulSoup
import requests
import pymongo
import time

urlPages = ['http://hz.xiaozhu.com/search-duanzufang-p{}-0/'.format(str(i)) for i in range(1,3)]
headers = {
    'Cookie':'abtest_ABTest4SearchDate=b; _xzsemtk=%7B%22ca_source%22%3A%22pcbaidusem%22%2C%22utm_term%22%3A%22%25E5%25B0%258F%25E7%258C%25AA%25E7%259F%25AD%25E7%25A7%259F%22%2C%22createtime%22%3A%222017-02-21+08%3A56%3A38%22%7D',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
}

def getUrls(urlPage,detailUrls):#通过导航页获取详情页链接
    flag = True
    while(flag):#超时重传
        try:
            webData = requests.get(urlPage,headers = headers,timeout = 1)
            flag = False
        except requests.exceptions.Timeout :
            print('time out,try again')
            pass
    soup = BeautifulSoup(webData.text,'lxml')
    urls = soup.select('#page_list a.resule_img_a')
    for u in urls:
        print(u.get('href'))
        detailUrls.append(u.get('href'))
    return detailUrls

def saveDetial(url,tab):#获取详情页信息并存入数据库
    time.sleep(1)
    flag = True
    while (flag):  # 超时重传
        try:
            webData = requests.get(url, headers=headers, timeout=1)
            flag = False
        except requests.exceptions.Timeout:
            print('time out,try again')
            pass
    soup = BeautifulSoup(webData.text, 'lxml')
    title = soup.select('div.pho_info > h4 > em')[0].text
    position = soup.select('div.pho_info > p > span')[0].text.strip()
    price = soup.select('#pricePart > div.day_l > span')[0].text
    name = soup.select('#floatRightBox > div.js_box.clearfix > div.w_240 > h6 > a')[0].get('title')
    data = {
        'title':title,
        'position':position,
        'price':int(price),
        'name':name
    }
    print(data)
    tab.insert_one(data)

client = pymongo.MongoClient('localhost',27017)
xiaozhu = client['xiaozhu']
sheet_tab = xiaozhu['sheet_tab']
detailUrls = []
for u in urlPages:
    detailUrls = getUrls(u,detailUrls)
for u in detailUrls:
    saveDetial(u, sheet_tab)

for item in sheet_tab.find({'price':{'$gte':500}}):#找出数据库中大于500的房源信息
    print(item)