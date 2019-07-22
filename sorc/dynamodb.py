# coding:utf-8

import boto3
from boto3.dynamodb.conditions import Attr, Key
from botocore.exceptions import ClientError
from manager import JsonManager

# create table
def create(dynamodb, tableName):
    table = dynamodb.create_table(
        TableName = tableName,
        KeySchema = [
            {
                'AttributeName': 'theme',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'theme_id',
                'KeyType': 'RANGE'
            },
        ],
        AttributeDefinitions = [
            {
                'AttributeName': 'theme',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'theme_id',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput = {
            'ReadCapacityUnits': 25,
            'WriteCapacityUnits': 25
        },
    )

    return table

# put item
def write(table, item):
    try:
        table.put_item(Item=item)
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("write succeeded!")

# put items
def batch_write(table, item_list):
    error_num = 0
    with table.batch_writer() as batch:
        for item in item_list:
            try:
                batch.put_item(Item=item)
            except ClientError as e:
                error_num += 1
                print(e.response['Error']['Message'])
                jsonManager = JsonManager()
                filename = '../data/error_{}_{}.json'.format(item['theme_id'], error_num)
                jsonManager.make_file(item, filename)
    if error_num == 0:
        print('all item write succeeded!')
    else:
        print('write error num: {}'.format(error_num))

# delete item
def delete(table, key):
    try:
        table.delete_item(Key=key)
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("item deleted!")

# get item
def get(table, key):
    item = None
    try:
        response = table.get_item(Key=key)
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        try:
            item = response['Item']
        except KeyError:
            print("That key is not exist!")
        else:
            print('get item succeeded!')

    return item

def search(table, key):
    pass

def scan(table):
    response = table.scan()
    data = response['Items']

    return data

def main():
    tableName = 'utanohi'
    key = {'theme_id': '1573d', 'theme': 'ハックルベリー'}
    dynamodb = boto3.resource(
        'dynamodb',
        region_name='ap-northeast-1',
        endpoint_url='http://localhost:8000',
        aws_access_key_id='ACCESS_ID',
        aws_secret_access_key='ACCESS_KEY')
    table = create(dynamodb, 'testTable')
    #table = create(dynamodb, tableName)
    #table = dynamodb.Table(tableName)
    #table = dynamodb.Table('testTable')
    #batch_write(table, item_list)
    #print(get(table, key))
    #delete(table, key)
    #table.delete()


if __name__ == "__main__":
    main()



"""
{
    "Items": [
        {
            "theme_id": {
                "S": "1246e"
            },
            "theme": {
                "S": "義務"
            },
            "tanka_num": {
                "N": "24"
            },
            "total_point": {
                "N": "28"
            },
            "tanka_info": {
                "L": [
                    {
                        "M": {
                            "love": {
                                "N": "6"
                            },
                            "Author": {
                                "S": "璃子"
                            },
                            "like": {
                                "N": "9"
                            },
                            "tanka": {
                                "S": "ワイシャツの白さにふっと立ち尽くす愛することも義務に思えて"
                            }
                        }
                    }
                ]
            }
        }
    }
}

key = {'theme_id': '437e', 'theme': '鉛筆'}
"""