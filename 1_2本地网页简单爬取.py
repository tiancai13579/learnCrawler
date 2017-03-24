from bs4 import BeautifulSoup
import re

info = []

with open('D:/code/python/studyWebCrawler/week1/1_2/1_2answer_of_homework/1_2_homework_required/index.html','r') as web_data:
    Soup = BeautifulSoup(web_data,'lxml')
    #print(Soup)
    images = Soup.select('body > div > div > div.col-md-9 > div > div > div > img')
    prices = Soup.select('body > div > div > div.col-md-9 > div > div > div > div.caption > h4.pull-right')
    titles = Soup.select('body > div > div > div.col-md-9 > div > div > div > div.caption > h4 > a')
    reviews = Soup.select('body > div > div > div.col-md-9 > div > div > div > div.ratings > p.pull-right')
    stars = Soup.select('body > div > div > div.col-md-9 > div > div > div > div.ratings > p:nth-of-type(2)')
    #print(images,prices,titles,reviews,stars,sep='\n-------------------------------\n')

for image,price,title,review,star in zip(images,prices,titles,reviews,stars):
    data = {
        'image':image.get('src'),
        'price':price.get_text(),
        'title':title.get_text(),
        'review':review.get_text(),
        'star':list(star.find_all(class_='glyphicon glyphicon-star'))
    }
    info.append(data)

#找评分高的
for i in info:
    if len(i['star']) > 4:
        print(i['title'],i['price'])

#找评论多的
for i in info:
    s,=re.findall(r'(\w*[0-9]+)\w*',i['review'])#正则表达式
    if float(s) > 20:
        print(i['title'],i['price'])