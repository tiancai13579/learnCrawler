from bs4 import BeautifulSoup
import requests
import pymongo
from multiprocessing import Pool
import random

client = pymongo.MongoClient('localhost',27017)
tongcheng58 = client['tongcheng58']
channel_url = tongcheng58['channel_url']
detailUrl = tongcheng58['detailUrl']
item_info = tongcheng58['item_info']

def getDetailUrl():#获取详情页url
    for u in channel_url.find():
        pageUrls = ['{}/pn{}'.format(u['url'],str(i)) for i in range(1,10)]#9页
        for pageUrl in pageUrls:
            flag = True
            while (flag):  # 超时重传
                try:
                    webData = requests.get(pageUrl)
                    flag = False
                except requests.exceptions.Timeout:
                    print('time out,try again')
                    pass
            soup = BeautifulSoup(webData.text, 'lxml')
            if soup.find('td','t'):#有这个字段，说明这页有东西
                for detUrl in soup.select('td.t a.t'):
                    detailUrl.insert_one({'url':detUrl.get('href')})
                    print(detUrl.get('href'))
            else:#这页没东西
                break

def get_item_info(url):
    proxy_list = [
        'http://125.88.74.122:83',
        'http://125.88.74.122:85',
        'http://125.88.74.122:82',
        'http://203.195.204.168:8080',
    ]
    try:
        proxy_ip = random.choice(proxy_list)
        proxies = {'http': proxy_ip}
        wb_data = requests.get(url,proxies=proxies)
        soup = BeautifulSoup(wb_data.text, 'lxml')
        try:
            no_longer_exist = '404' in soup.find('script', type="text/javascript").get('src').split('/')
        except:
            no_longer_exist = False
        try:
            xiajia = '商品已下架' in soup.select('span.soldout_btn')[0].text
        except:
            xiajia = False
        if no_longer_exist:
            print('这个页面不见啦！！')
            pass
        elif xiajia:
            print('下架啦！！')
            pass
        else:
            try:
                title = soup.select('div.col_sub.mainTitle h1')[0].text
                price = soup.select('span.price.c_f50')[0].text
                date = soup.select('ul.mtit_con_left.fl li.time')[0].text
                area = list(soup.select('.c_25d a')[-1].stripped_strings) if soup.find_all('span', 'c_25d') else None
                item_info.insert_one({'title': title, 'price': price, 'date': date, 'area': area, 'url': url})
                print({'title': title, 'price': price, 'date': date, 'area': area, 'url': url})
            except:
                print('呃，有些网页不一样，趴不了')
                pass
    except:
        print('好吧，我也不知道哪里错了，就跳过吧')
        pass


if __name__ == '__main__':

    #getDetailUrl()
    urls = []
    for i in detailUrl.find():
        urls.append(i['url'])
    pool = Pool()
    pool.map(get_item_info,urls)#多进程获取
