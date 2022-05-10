from constants import RECIPIENTS
from dynamo_service import save_transactions
from email_service import send_email
from process_csv import get_balance, save_csv_tmp
from s3_service import get_csv_from_s3


def lambda_handler(event, context):
    data = event["Records"][0]

    bucket_name = data["s3"]["bucket"]["name"]
    file_name = data["s3"]["object"]["key"]

    csv_obj = get_csv_from_s3(bucket_name, file_name)
    csv_file = csv_obj.read().decode("utf-8").splitlines()

    save_transactions(csv_file)

    filename_csv = save_csv_tmp(csv_file)
    balance = get_balance(csv_file)

    print("sending email")
    send_email("Transactions Resume", RECIPIENTS, balance, filename_csv)
    print("sending email successful")

    return {"success": True}
