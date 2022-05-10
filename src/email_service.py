import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Dict, List

import jinja2

from constants import HOST_EMAIL, PASSWORD, PORT_EMAIL, USERNAME


def render_template(template, params):
    if not os.path.exists(template):
        raise FileNotFoundError

    template_loader = jinja2.FileSystemLoader(searchpath="./")
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template(template)

    return template.render(params)


def send_email(
    subject: str,
    recipients: List[str],
    params: Dict,
    filename_csv: str,
    template_name: str = "./email_transactions.j2",
):
    html = str(render_template(template_name, params))

    message = MIMEMultipart("alternative")
    message["From"] = USERNAME
    message["Subject"] = subject
    message["To"] = ",".join(recipients)
    message.attach(MIMEText(html, "html"))

    try:
        attach_file(filename_csv, message)
    except Exception as error:
        print(error)
    server = smtplib.SMTP(HOST_EMAIL, PORT_EMAIL)

    try:
        server.starttls()
        server.login(USERNAME, PASSWORD)
        server.sendmail(USERNAME, recipients, message.as_string())
    except Exception as error:
        print(error)
    finally:
        server.quit()


def attach_file(filename_csv, message):
    attach_file = open(f"/tmp/{filename_csv}", "rb")
    payload = MIMEBase("application", "csv", Name="transaction.csv")
    payload.set_payload((attach_file).read())
    encoders.encode_base64(payload)
    payload.add_header(
        "Content-Decomposition", "attachment", filename="transaction.csv"
    )
    message.attach(payload)
    print("attach sucess")
