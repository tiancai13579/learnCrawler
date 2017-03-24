#把瓦尔登湖写入mongodb数据库
import pymongo

client = pymongo.MongoClient('localhost',27017)#建立和mongodb连接
walden = client['walden']#创建一个叫walden的数据库
sheet_tab = walden['sheet_tab']#创建一个叫sheet_tab的表单
'''
#写入一次就行了，别多次写入
path = 'walden.txt'
with open(path,'r') as f:
    lines = f.readlines()
    for index,line in enumerate(lines):#既要索引，又要元素，用enumerate进行枚举
        data = {
            'index':index,
            'line':line,
            'words':len(line.split())
        }
        sheet_tab.insert_one(data)#往表单中添加内容
'''
for item in sheet_tab.find():#全部打印
    print(item)

for item in sheet_tab.find({'words':0}):#打印没字的
    print(item['index'])

#mongodb操作  $lt/$lte/$gt/$gte/$ne，依次等价于</<=/>/>=/!=。（l表示less g表示greater e表示equal n表示not  ）

for item in sheet_tab.find({'words':{'$gt':16}}):#打印字数大于16的
    print(item['line'])

path = 'walden.txt'
with open(path,'r') as f:
    lines = f.readlines()
    for index,line in enumerate(lines):#既要索引，又要元素，用enumerate进行枚举
        data = {
            'index':index,
            'line':line,
            'words':len(line.split())
        }
        sheet_tab.insert_one(data)#往表单中添加内容