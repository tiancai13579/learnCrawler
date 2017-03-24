from bs4 import BeautifulSoup
import requests,urllib.request,time

url = ['https://knewone.com/?page={}'.format(str(i)) for i in range(1,5)]
headers = {
    'user-agent':'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Mobile Safari/537.36',
    #'cookie':'gr_user_id=84657550-6696-4b79-b53b-18d5efca63f8; _gat=1; _ga=GA1.2.1745982069.1487656670; Hm_lvt_b44696b80ba45a90a23982e53f8347d0=1487656671,1487675466,1487675480,1487675493; Hm_lpvt_b44696b80ba45a90a23982e53f8347d0=1487675493; _knewone_v2_session=RlA0ZUN6MUNNNE5DQ1NVZzVVc1JCeHNOOENiTWd3ZkNDOXpnR2w2MVNBMEh1L1FQSVBPYVFzZlRVc0xpMlBmeHFHT1RNZ3ZxOE4yQUJQMUJtM1piamlpVkMwTlYxblF1dlF0ZlFwN2ZqUGwwa3lNaktYSDZ6WS8rYmJkQXBROWg4a0JleFQrTE9wN3dSTU5FSFh4eFNyZStqa2lSOERzL1FoanpaOU9sOUN0eHB6aXdCWEMyb3p2Y0lBWTJJY24vLS1tSnNaTUU4KyszWWs1WHZuczkxUENRPT0%3D--38a8041fdc51b4709b07690efa67c52f37a27a3d; gr_session_id_e7b7e334c98d4530928513e7439f9ed2=cbed78dc-32c1-4bbb-ab98-9853f3939112'
}
#wrapper > section > div:nth-child(3) > div > section > div.thumbnail-cover > a > img
def getPicUrl(url,imgUrlAll):
    web_data = requests.get(url,headers=headers)
    soup = BeautifulSoup(web_data.text,'lxml')
    img = soup.select('div.thumbnail-cover > a > img')
    for i in img:
        imgurl = i.get('src')[0:-7]#剔除链接最后7个干扰字符
        imgUrlAll.append(imgurl)
    return imgUrlAll

imgUrlAll=[]
path = 'C://Users/Tiancai/Desktop/Test/'
for u in url:
    print(u)
    imgUrlAll = getPicUrl(u,imgUrlAll)
for i in imgUrlAll:
    time.sleep(1)
    print(i)
    urllib.request.urlretrieve(i,path+i[-10:])#下载图片，文件命名结尾为最后10个字母
