import boto3

from typing import List

from process_csv import get_balance


def get_csv_from_s3(bucket_name, csv_name) -> List[str]:
    s3 = boto3.resource('s3')
    s3_obj =  s3.Object(bucket_name, csv_name)
    return s3_obj.get()['Body'].read().decode('utf-8').splitlines()


def lambda_handler(event, context):
    data = event['Records'][0]

    bucket_name = data['s3']["bucket"]["name"]
    file_name = data['s3']['object']['key']


    csv_file = get_csv_from_s3(bucket_name, file_name)
    print(csv_file)
    balance = get_balance(csv_file)
    print(balance)

    return {"success": True}