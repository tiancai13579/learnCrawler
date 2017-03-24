from bs4 import BeautifulSoup
import requests
import time

url_fav = 'https://www.tripadvisor.cn/Saves/all'
url = 'http://www.tripadvisor.cn/Attractions-g60763-Activities-New_York_City_New_York.html'
urls = ['http://www.tripadvisor.cn/Attractions-g60763-Activities-oa{}-New_York_City_New_York.html'.format(str(i)) for i in range(30,930,30)]
#手机端反爬会弱一些
phoneHeaders = {
    'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1',
    'Cookie':'TASSK=enc%3AADULRnwUse6yDAr2TLJ78pfans8XOoVAMjQDJjMU0F9zIcoU99Ml5Vfr6UqBVya%2FwLBQ0RB70Lui8P7aR%2FhePMhh7p87biLwuGzUUVYhfRLVfW9xaG5HjRtWk3PoXR0TOg%3D%3D; TAUnique=%1%enc%3AmmhQt8DSwe4ANkey5Q9gsUPKp9lDxkUo42z6s%2Frx9Zo%3D; ServerPool=R; _jzqckmp=1; __gads=ID=d56d180ff9dc570c:T=1487592973:S=ALNI_MYFQJMvc_IDLUyo1aohkXp75Dg8OA; TAPD=tripadvisor.cn; CommercePopunder=SuppressAll*1487593197679; _smt_uid=58aade06.c33062a; interstitialCounter=2; MobileLastViewedList=%1%%2FAttractions-g60763-Activities-oa30-New_York_City_New_York.html; taMobileRV=%1%%7B%2210028%22%3A%5B60763%5D%7D; bdshare_firstime=1487596609244; SecureLogin2=3.4%3AADWGnr4%2F0f50cRLimOdnZIThg3WWRNbae2V6q7stQ%2BC0AddWdAaI7HBkB%2BIQhJcD0ykKG%2B81RRpAhZ7KILU6hBxwhRiZD3v2U3BR35CaYL5s3HfDJmOgJafJ%2BDwVu4GcVMruhqcYelZUYoFoPvN%2BzFXgtEzO%2FuC0BOTLqQfruqOnxt9HCJNDynSyjeN0uRMS8hoN2pQhdZf9FO9I24I1UlA%3D; TAAuth2=%1%3%3A4167f328261234a99f2cb11f6190a4e4%3AAGGnOOfL4ojOfZwrBfHz00xOd9zMtqF7RzLtYd7p%2FFiT9f%2FzmCCSKPi7JDik3%2F1A5hfYdAogoidx92%2FSUkUzMII2aMlXR9puVrw1ZeCzcHpa7GDS2U64UyeNyEUeANLWvpf3V3C3i%2FsKaY7pIiHGw%2BWm1dJIHc3Reuqkxds4k2FJgKAJPSRxh1IG9op7e106wwMoVdjG6gWgQOWeDePBn5koIa%2BweG9RXM4fKGUbRqZl; TATravelInfo=V2*A.2*MG.-1*HP.2*FL.3*RVL.210108_51l60763_51l298566_51l298184_51l479258_51l1373780_51; CM=%1%HanaPersist%2C%2C-1%7CPremiumMobSess%2C%2C-1%7Ct4b-pc%2C%2C-1%7CHanaSession%2C%2C-1%7CRCPers%2C%2C-1%7CWShadeSeen%2C%2C-1%7CFtrPers%2C%2C-1%7CTheForkMCCPers%2C%2C-1%7CHomeASess%2C2%2C-1%7CPremiumSURPers%2C%2C-1%7CPremiumMCSess%2C%2C-1%7Csesscoestorem%2C%2C-1%7CCCSess%2C%2C-1%7CViatorMCPers%2C%2C-1%7Csesssticker%2C%2C-1%7C%24%2C%2C-1%7CPremiumORSess%2C%2C-1%7Ct4b-sc%2C%2C-1%7CMC_IB_UPSELL_IB_LOGOS2%2C%2C-1%7Cb2bmcpers%2C%2C-1%7CMC_IB_UPSELL_IB_LOGOS%2C%2C-1%7CPremMCBtmSess%2C%2C-1%7CPremiumSURSess%2C%2C-1%7CLaFourchette+Banners%2C%2C-1%7Csess_rev%2C%2C-1%7Csessamex%2C%2C-1%7Cperscoestorem%2C%2C-1%7CPremiumRRSess%2C%2C-1%7CSaveFtrPers%2C%2C-1%7CTheForkRRSess%2C%2C-1%7Cpers_rev%2C%2C-1%7CMetaFtrSess%2C%2C-1%7Cmds%2C%2C-1%7CRBAPers%2C%2C-1%7CWAR_RESTAURANT_FOOTER_PERSISTANT%2C%2C-1%7CFtrSess%2C%2C-1%7CHomeAPers%2C%2C-1%7CPremiumMobPers%2C%2C-1%7CRCSess%2C%2C-1%7CLaFourchette+MC+Banners%2C%2C-1%7Cbookstickcook%2C%2C-1%7Csh%2C%2C-1%7Cpssamex%2C%2C-1%7CTheForkMCCSess%2C%2C-1%7CCCPers%2C%2C-1%7CWAR_RESTAURANT_FOOTER_SESSION%2C%2C-1%7Cb2bmcsess%2C%2C-1%7CViatorMCSess%2C%2C-1%7CPremiumMCPers%2C%2C-1%7CPremiumRRPers%2C%2C-1%7CPremMCBtmPers%2C%2C-1%7CTheForkRRPers%2C%2C-1%7CSaveFtrSess%2C%2C-1%7CPremiumORPers%2C%2C-1%7CRBASess%2C%2C-1%7Cbookstickpers%2C%2C-1%7Cperssticker%2C%2C-1%7CMetaFtrPers%2C%2C-1%7C; TAReturnTo=%1%%2FAttraction_Review-g1066456-d1373780-Reviews-Meiji_Jingu_Shrine-Shibuya_Tokyo_Tokyo_Prefecture_Kanto.html; ki_t=1487596611331%3B1487596611331%3B1487597115907%3B1%3B7; ki_r=; roybatty=TNI1625!AGCvXFe9QFfMEtzIGZp6jzG151rD7kVX8xCu072Tn4QlvCcDt3aBi128lg9K00mBccFohhJsnUCH3Cb7Og5%2FO%2BIrYUTZLchxe98DcDpWsUJ6KHshhr4x2ypEjKggIMCJBbEiZtS960JyTbxH7qLKBG5thH3c7x2VWbWilnltLGe5%2C1; TASession=%1%V2ID.A10F9AE04A12B9D11245213EF8A492CE*SQ.85*LP.%2F*PR.427%7C*LS.PerformancePingback*GR.90*TCPAR.16*TBR.84*EXEX.53*ABTR.52*PPRP.57*PHTB.55*FS.30*CPU.15*HS.popularity*ES.popularity*AS.popularity*DS.5*SAS.popularity*FPS.oldFirst*TS.9554D60C15DACA32318640E4B7B9C06D*LF.zhCN*FA.1*DF.0*MS.-1*RMS.-1*FLO.298184*TRA.true*LD.1373780; TAUD=LA-1487592966971-1*LG-4186989-2.0.F.*LD-4186990-.....; Hm_lvt_2947ca2c006be346c7a024ce1ad9c24a=1487592966; Hm_lpvt_2947ca2c006be346c7a024ce1ad9c24a=1487597152; _qzja=1.676981224.1487592966788.1487592966788.1487592966789.1487597139788.1487597152454..0.0.19.1; _qzjb=1.1487592966789.19.0.0.0; _qzjc=1; _qzjto=19.1.0; _jzqa=1.892438706273310600.1487592967.1487592967.1487592967.1; _jzqc=1; _jzqb=1.19.10.1487592967.1'
    #'User-Agent':'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Mobile Safari/537.36'
}
def get_attractions(url,data=None):
    time.sleep(1)
    web_data = requests.get(url,headers=phoneHeaders)
    soup = BeautifulSoup(web_data.text,'lxml')#保存成文本格式
    # print(soup)
    images = soup.select('img[width="54"]')#即使用了手机端还是被反扒了
    titles = soup.select('div.container.containerLLR > div.title.titleLLR > div')
    cates = soup.select('div.container.containerLLR > div.attraction_types > span')
    #print(titles,cates,sep = '\n---------------------------------------------------\n')
    if data == None:
        for title,cate in zip(titles,cates):
            s = cate.get_text()
            data={
                'title':title.get_text(),
                'cate':s.split(', ')
            }
            print(data)

get_attractions(url)
for i in urls:
    get_attractions(i)

