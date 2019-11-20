import json
import xlrd
import os
import xlwt

date = '11.20'  # 存放林火办的txt数据
baiDu = '20191120.czml'  # 百度产品
# 第一步是将林火数据整合到表格中
office_fires_url = r'C:\Users\zwish\Desktop\fire\林火办\\' + date
office_fires_array = []
for root, dirs, files in os.walk(office_fires_url):
    for file in files:
        if (file[-3:]) == 'txt':
            with open((root + '/' + file), 'r', encoding='utf-8') as f:
                data = json.loads(f.read())
                for item in data['rows']:
                    fire = {
                        'ImageDate': item['ImageDate'],
                        'Longitude': item['Longitude'],
                        'Latitude': item['Latitude'],
                        'HotspotType': item['HotspotType']
                    }
                    office_fires_array.append(fire)
# 将林火办的火点输出
office_fires_workbook = xlwt.Workbook(office_fires_url)
office_fires_sheet = office_fires_workbook.add_sheet(date)
office_fires_title = ['系统接收时间', '经度', '纬度', '火点类型']
office_fires_save_path = office_fires_url

for index, titleName in enumerate(office_fires_title):
    office_fires_sheet.write(0, index, titleName)

for index, fire in enumerate(office_fires_array):
    office_fires_sheet.write(index + 1, 0, fire['ImageDate'])
    office_fires_sheet.write(index + 1, 1, fire['Longitude'])
    office_fires_sheet.write(index + 1, 2, fire['Latitude'])
    office_fires_sheet.write(index + 1, 3, fire['HotspotType'])

office_fires_workbook.save(office_fires_url + '\\' + date + '.xls')

# 读取百度的火点
baidu_fires_url = r'C:\Users\zwish\Desktop\fire\baidu林火\\' + baiDu
baidu_fires_array = []
with open(baidu_fires_url, 'r', encoding='utf-8') as f:
    data = json.loads(f.read())
    for item in data:
        if 'position' in item:
            fire = {
                'lon': item['position']['cartographicDegrees'][0],
                'lat': item['position']['cartographicDegrees'][1],
                'brightness': item['description'].split(',', 1)[0][11:],
                'confidence': item['description'].split(',', 1)[1][11:],
            }
            baidu_fires_array.append(fire)

# 对比两个火点
onFires = []
Index = []
for officeIndex, officeFire in enumerate(office_fires_array):
    for baiDuIndex, baiDuFire in enumerate(baidu_fires_array):
        difLon = abs(officeFire['Longitude'] - baiDuFire['lon'])
        difLat = abs(officeFire['Latitude'] - baiDuFire['lat'])
        if difLat <= 0.1 and difLon <= 0.1:
            onFires.append([baiDuFire, officeFire, difLon, difLat])
            Index.append([officeIndex, baiDuIndex])


def filteFire(fire):
    not_belong = True
    index = 0
    if 'ImageDate' in fire:
        index = 1
    elif 'brightness' in fire:
        index = 0
    for f in onFires:
        if f[index] == fire:
            not_belong = False
    return not_belong


leftForestOfficeFires = list(filter(filteFire, office_fires_array))
leftBaiDuFires = list(filter(filteFire, baidu_fires_array))
# print(leftForestOfficeFires)
# print(leftBaiDuFires)

for fire in leftBaiDuFires:
    onFires.append([fire, {
        'ImageDate': '',
        'Longitude': '',
        'Latitude': '',
        'HotspotType': '',
    }, '', ''])

for fire in leftForestOfficeFires:
    onFires.append([{
        'lon': '',
        'lat': '',
        'brightness': '',
        'confidence': '',
    }, fire, '', ''])

print(onFires)

titles = ['百度火点日产品', '林火办', '分析']

names = ['系统发现时间', '经度', '纬度', '亮度值', '置信度', '关注度指数', '系统发现时间', '经度', '纬度', '火点类型', '百度是否命中（Y/N）', '经度误差', '纬度误差']

# 存放最终的结果
resultPath = r'C:\Users\zwish\Desktop\fire\对比结果\\'
resultBook = xlwt.Workbook(resultPath)
resultSheet = resultBook.add_sheet('result')
resultSheet.write(0, 3, titles[0])
resultSheet.write(0, 7, titles[1])
resultSheet.write(0, 11, titles[2])
for index, name in enumerate(names):
    resultSheet.write(1, index, name)

for index, fire in enumerate(onFires):
    print(fire)
    resultSheet.write(index + 2, 1, fire[0]['lon'])
    resultSheet.write(index + 2, 2, fire[0]['lat'])
    resultSheet.write(index + 2, 3, fire[0]['brightness'])
    resultSheet.write(index + 2, 4, fire[0]['confidence'])
    resultSheet.write(index + 2, 6, fire[1]['ImageDate'])
    resultSheet.write(index + 2, 7, fire[1]['Longitude'])
    resultSheet.write(index + 2, 8, fire[1]['Latitude'])
    resultSheet.write(index + 2, 9, fire[1]['HotspotType'])
    resultSheet.write(index + 2, 11, fire[2])
    resultSheet.write(index + 2, 12, fire[3])

baidu_alarm_url = r'C:\Users\zwish\Desktop\fire\警报\\' + date
baidu_alarm_array = []
for root, dirs, files in os.walk(baidu_alarm_url):
    for file in files:
        if (file[-3:]) == 'csv':
            with open((root + '/' + file), 'r', encoding='utf-8') as f:
                data = f.read().split(',')
                print(data)
                fire = {
                    'cur_dataetime': data[13],
                    'start_datatime': data[14],
                    'longtitude': data[15],
                    'latitude': data[16],
                    'address': data[17],
                    'brightness': data[18],
                    'pixel_count': data[19],
                    'frame_count': data[20],
                    'area': data[21],
                    'confidence': data[22],
                    'attention_value': data[23],
                }
                baidu_alarm_array.append(fire)
print(baidu_alarm_array)

sheet = resultBook.add_sheet(date + 'alarm')
sheet.write(1, 1, 'cur_dataetime')
sheet.write(1, 2, 'start_datatime')
sheet.write(1, 3, 'longtitude')
sheet.write(1, 4, 'latitude')
sheet.write(1, 5, 'address')
sheet.write(1, 6, 'brightness')
sheet.write(1, 7, 'pixel_count')
sheet.write(1, 8, 'frame_count')
sheet.write(1, 9, 'area')
sheet.write(1, 10, 'confidence')
sheet.write(1, 11, 'attention_value')

for index, fire in enumerate(baidu_alarm_array):
    sheet.write(index + 2, 1, fire['cur_dataetime'])
    sheet.write(index + 2, 2, fire['start_datatime'])
    sheet.write(index + 2, 3, fire['longtitude'])
    sheet.write(index + 2, 4, fire['latitude'])
    sheet.write(index + 2, 5, fire['address'])
    sheet.write(index + 2, 6, fire['brightness'])
    sheet.write(index + 2, 7, fire['pixel_count'])
    sheet.write(index + 2, 8, fire['frame_count'])
    sheet.write(index + 2, 9, fire['area'])
    sheet.write(index + 2, 10, fire['confidence'])
    sheet.write(index + 2, 11, fire['attention_value'])

resultBook.save(resultPath + date + '.xls')
