from typing import List

import boto3

def get_csv_from_s3(bucket_name, csv_name) -> List[str]:
    s3 = boto3.resource('s3')
    s3_obj =  s3.Object(bucket_name, csv_name)
    return s3_obj.get()['Body']
