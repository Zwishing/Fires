import os
import json
import csv

alarm_url = r'C:\Users\zwish\Desktop\fire\警报\11.20'
fieldnames = ('id', 'latitude', 'longitude', 'start_datetime', 'start_sys_datetime', 'end_datetime',
              'end_sys_datetime', 'pixel_count', 'area', 'address', 'province', 'city', 'district',
              'remote_sensing', 'brightness', 'confidence', 'attention_value', 'is_alarm', 'alarm_times',
              'start_alarm_rs_datetime', 'start_alarm_sys_datetime', 'release_datetime')
for root, dirs, files in os.walk(alarm_url):
    for file in files:
        with open((root + '/' + file), 'r', encoding='utf-8') as f:
            if file.split('.')[1] == 'csv':
                reader = csv.DictReader(f, fieldnames)
                for row in reader:
                    print(row['is_alarm'])

                # data = f.read().split(',')
                # for str in data:
                #     print(str)
            elif file.split('.')[1] == 'json':
                data = f.read()
                print(data)
