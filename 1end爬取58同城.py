from bs4 import BeautifulSoup
import requests
import re

pageUrl = 'http://bj.58.com/shouji/?PGTID=0d200005-0000-13e3-ffc7-fd00f60aed6f&ClickID=1'
testUrl = 'http://bj.58.com/shouji/29095987657521x.shtml?psid=123693094194993687605641037&entinfo=29095987657521_0'
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Cookie':'f=n; id58=XBJWv1ir4BM0o7SqoWOxRA==; mcity=nb; ipcity=nb%7C%u5B81%u6CE2%7C0; als=0; commonTopbar_myfeet_tooltip=end; 58home=bj; commontopbar_city=1%7C%u5317%u4EAC%7Cbj; bj58_id58s="YnU4bG1VdzRVNV9BNTA1Nw=="; final_history=26088204291258; myfeet_tooltip=end; bdshare_firstime=1487659158653; sessionid=66f8a9b8-ead0-4418-a63c-cee95df7e051; city=bj; bj58_new_session=0; bj58_init_refer="http://bj.58.com/pbdn/0/"; bj58_new_uv=2; 58tj_uuid=06acb4ca-1d1d-4324-bd74-120d16d72aa0; new_session=0; new_uv=2; utm_source=; spm=; init_refer=http%253A%252F%252Fbj.58.com%252Fpbdn%252F0%252F; f=n'
}

#获取想要的详情页的链接函数
def getDetailUrl(pageUrl,urls):
    web_data = requests.get(pageUrl,headers = headers)
    soup = BeautifulSoup(web_data.text,'lxml')
    data = soup.select('#zhiding > tbody > tr > td.t > a')
    for i in data:
        #print(i)
        url = i.get('href')
        urls.append(url)
    return urls

def get_views_from(url):
    id = url.split('/')[-1].split('x.shtml')[0]
    api = 'http://jst1.58.com/counter?infoid={}&userid=0&uname=&sid=0&lid=1&px=&cfpath=5,36'.format(id)
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'Cookie':'id58=XBJWv1ir4BM0o7SqoWOxRA==; mcity=nb; als=0; commonTopbar_myfeet_tooltip=end; 58home=bj; bj58_id58s="YnU4bG1VdzRVNV9BNTA1Nw=="; final_history=26088204291258; myfeet_tooltip=end; es_ab=1; city=bj; ipcity=nb%7C%u5B81%u6CE2; sessionid=93f3536d-29b6-4958-8617-277ba83d6f8e; 58tj_uuid=06acb4ca-1d1d-4324-bd74-120d16d72aa0; new_session=0; new_uv=5; utm_source=; spm=; init_refer=; bj58_new_session=0; bj58_init_refer=""; bj58_new_uv=5',
        'Host': 'jst1.58.com',
        'Referer':'url',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
    }
    js = requests.get(api,headers = headers)#请求解析,防止反爬，必须要完整的headers
    views = js.text.split('=')[-1]
    return views

#获取商品详情
def getDetail(url,info):
    web_data = requests.get(url,headers = headers)
    soup = BeautifulSoup(web_data.text,'lxml')
    #print(soup)
    title = soup.select('#content h1')[0].text
    price = soup.select('span.price')[0].text
    date =  soup.select('#content li.time')[0].text
    quality = soup.select('#content > div.person_add_top.no_ident_top > div.per_ad_left > div.col_sub.sumary > ul > li:nth-of-type(2) > div.su_con > span')[0].text.strip()
    classification = soup.select('#header > div.breadCrumb.f12 > span:nth-of-type(3) > a')[0].text.strip()
    views = get_views_from(url)
    #print(title,price,date,quality,classification,sep = '\n----------------------\n')
    data = {
        'title':title,
        'price':price,
        'date':date,
        'quality':quality,
        'classification':classification,
        'views':views
    }
    print(data)
    info.append(data)
    return info

urls = []
info = []
urls = getDetailUrl(pageUrl,urls)
for u in urls:
    info = getDetail(u, info)
