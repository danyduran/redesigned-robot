import logging

from typing import List

import boto3

from constants import COLUMNS

DYNAMO_DB = boto3.resource("dynamodb")

table_transactions = DYNAMO_DB.Table("transactions")


def save_transactions(transactions: List[str]):
    logging.info("creating")
    for transaction in transactions[1:]:
        transaction = transaction.split(",")
        transaction_dict = {
            "id": transaction[COLUMNS["id"]],
            "date": transaction[COLUMNS["date"]],
            "transaction": transaction[COLUMNS["transaction"]],
        }
        table_transactions.put_item(Item=transaction_dict)
    logging.info("creating successful")


def get_transactions():
    response = table_transactions.scan()
    data = response["Items"]

    logging.debug(data)

    return data
