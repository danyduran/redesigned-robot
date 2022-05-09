import csv
from random import choice
from string import ascii_letters




from datetime import datetime

from constants import COLUMNS, FORMAT_DATE, FORMAT_MONTH, LEN_WORD


def generate_name_file():
    return "".join(choice(ascii_letters) for _ in range(LEN_WORD))


def save_csv_tmp(csv_data):
    filename= generate_name_file()
    FILENAME = f"/tmp/{filename}.csv"

    with open(FILENAME, 'w') as csvfile:
        headers =csv_data[0].split(",")
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(headers)
        csvwriter.writerows([row.split(",") for row in csv_data[1:]])

    return f"{filename}.csv"


def get_balance(file):

    balance = {
        "total": 0,
        "average_debit": 0,
        "average_credit": 0,
        "total_debit": 0,
        "total_credit": 0,
        "count_debit_operation": 0,
        "count_credit_operation": 0,
        "transactions_month": {}
    }

    csv_file = csv.reader(file, delimiter = ',')
    next(csv_file, None)

    for row in csv_file:
        date_str = row[COLUMNS["date"]]
        transaction_str = row[COLUMNS["transaction"]]
        operation = transaction_str[:1]
        amount = float(transaction_str[1:])

        if operation == "+":
            balance["count_credit_operation"] += 1
            balance["total_credit"] += amount
            balance["total"] += amount
        elif operation == "-":
            balance["total"] -= amount
            balance["total_debit"] -= amount
            balance["count_debit_operation"] += 1

        date = datetime.strptime(date_str, FORMAT_DATE)
        month = datetime.strftime(date, FORMAT_MONTH)

        balance["transactions_month"].setdefault(month, 0)
        balance["transactions_month"][month] += 1

    balance["average_credit"] = balance["total_credit"] / balance["count_credit_operation"]
    balance["average_debit"] = balance["total_debit"] / balance["count_debit_operation"]

    return balance

