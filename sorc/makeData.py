# coding:utf-8

import re
import dynamodb
import json
import decimal

from manager import JsonManager

NO_USE_THEME = ['自由律', '超自由詠']

def makeAllTankaJson(table):
    response = table.scan()
    data = response["Items"]
    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])

    data_list = []
    counter = 0
    for item in data:
        counter += 1
        if item['theme'] in NO_USE_THEME:
            continue
        tanka_data = {'theme':None, 'tanka_list':[]}
        tanka_data['theme'] = item['theme']
        for tanka_info in item['tanka_info']:
            tanka = re.sub(r'<rt>.+?</rt>', '', tanka_info['tanka'])
            tanka = re.sub(r'<.+?>', '', tanka)
            tanka_info = {'tanka':tanka, 'love':tanka_info['love'], 'like':tanka_info['like']}
            tanka_data['tanka_list'].append(tanka_info)
        data_list.append(tanka_data)

    json = {"all":data_list}
    jsonManager = JsonManager()
    jsonManager.make_file(json, '../data/tankaText.txt')

    print(counter)

def main():
    tableName = 'utanohi'
    table = dynamodb.getTable(tableName)
    makeAllTankaJson(table)


if __name__ == "__main__":
    main()