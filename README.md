
This mvp is built using terraform to building the infrastructure on AWS, specifically a bucket on s3 and lambda(using python3 as language)

```
.
└── redesigned-robot/
    ├── src/
    │   ├── aws_service.py
    │   ├── constants.py
    │   ├── email_service.py
    │   ├── email_transactions.j2
    │   ├── main.py
    │   ├── pip.sh
    │   ├── process_csv.py
    │   └── requirements.txt
    ├── main.tf
    └── variables.tf
```


# How it works?

Every time when a csv file is uploaded into the s3 bucket, the bucket launch a event to invoke the lambda, then when the lambda is invoked receives the event that contains the bucket name and the key of the object(csv filename), getting the csv from the s3, process the file, save it in tmp directory of lambda(the lambdas don't have a filesystem that allows WRITE operations, only READ operations) and finally sending the email with the resume of balance and the csv file that store in the tmp directory.


# A big picture of structure

The terraform files main.tf and variables.tf help to create a s3 that invoke the lambda to process a new csv when is uploaded.
![Diagram](https://user-images.githubusercontent.com/28666420/167497625-55f5dab1-fc4f-4606-96fb-c008d7ff5908.png)


# How install the project
So, you need to have a aws account(configured the aws cli on your computer), terraform installed too. obviousy the this project cloned in your computer.
Once you haved installed and configured the aws cli and terraform, just follow the next steps

Steps:
- search into the project a file called constants.py, look the constant RECIPIENTS and add your email to receive the email
- change into the directory where main.tf is in
- run terraform init
- run terraform apply

Terraform apply could take a few minutes to create the infra on aws, once all the infrastructure is created, go to your account of aws, and find the new s3 bucket and uploaded a csv file, this trigger the lambda that will send you the email with balance the csv file as a attachment
