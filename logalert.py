#!/usr/bin/env python3

import argparse
import json
import smtplib
from email.message import EmailMessage

DEFAULT_CONFIG = 'config.json'

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-c", "--config", help="Set config file. Example: config.json", type=str, default=DEFAULT_CONFIG)

args = parser.parse_args()


class LogEmail():

    subject = f'CF log alert'

    def __init__(self, json_email):
        self.smtp_url = json_email['smtp_url']
        self.smtp_port = json_email['smtp_port']
        self.sender_email = json_email['sender_email']
        self.receiver_email = json_email['receiver_email']

    def send_email(self, message):
        msg = EmailMessage()
        msg.set_content(message)
        msg['Subject'] = self.subject
        msg['From'] = self.sender_email
        msg['To'] = self.receiver_email

        with smtplib.SMTP(self.smtp_url, self.smtp_port) as m:
            m.send_message(msg)


try:
    with open(args.config, 'r') as json_file:
        config_json = json.load(json_file)
except (FileNotFoundError, IOError, json.decoder.JSONDecodeError):
    print("Wrong config file or path. ")


le = LogEmail(config_json['email'])
le.send_email('test')
