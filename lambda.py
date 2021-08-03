import json
import urllib.parse
import boto3
import pandas as pd
print('Loading function')

s3 = boto3.client('s3')


def is_anagram(s1, s2):
    return sorted(s1.lower()) == sorted(s2.lower())


def lambda_handler(event, context):

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(
        event['Records'][0]['s3']['object']['key'], encoding='utf-8')

    result = []

    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        df = pd.read_csv(io.BytesIO(response['Body'].read()))

        for _, row in df.iterrows():
            result.append((row["string1"], row["string2"],
                          is_anagram(row["string1"], row["string2"])))

        return result
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
