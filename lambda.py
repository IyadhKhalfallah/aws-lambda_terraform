import json
import urllib.parse
import boto3

s3 = boto3.client('s3')


def is_anagram(string_1, string_2):
    return sorted(string_1.lower()) == sorted(string_2.lower())


def lambda_handler(event, context):

    # Geting the object from the event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(
        event['Records'][0]['s3']['object']['key'], encoding='utf-8')

    # Initializing the result array, where anagram outputs will be stored
    result = []

    try:
        response = s3.get_object(Bucket=bucket, Key=key)

        # Reading the anagram.csv file
        content = response["Body"].read().decode('utf-8')

        for elem in content.split('\r'):
            strings = elem.split(';')
            strings[0] = strings[0].replace('\n', '')
            strings[1] = strings[1].replace('\n', '')
            result.append(is_anagram(strings[0], strings[1]))

        return result
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}.'.format(key, bucket))
        raise e
