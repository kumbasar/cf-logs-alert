#!/usr/bin/env python3

import argparse
import json
import smtplib
import cf_api
from email.message import EmailMessage

DEFAULT_CONFIG = 'config.json'

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-c", "--config", help="Set config file. Example: config.json", type=str, default=DEFAULT_CONFIG)

args = parser.parse_args()


class EmailAlert():

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


class CFLOG():

    deploy_client_id = 'cf'
    deploy_client_secret = ''
    verify_ssl = True

    def __init__(self, json_cf, mail):
        self.mail = mail

        self.cc = cf_api.new_cloud_controller(
            json_cf['cloud_controller'],
            client_id=self.deploy_client_id,
            client_secret=self.deploy_client_secret,
            username=json_cf['cfuser'],
            password=json_cf['cloud_controller']).set_verify_ssl(verify_ssl)


try:
    with open(args.config, 'r') as json_file:
        config_json = json.load(json_file)
except (FileNotFoundError, IOError, json.decoder.JSONDecodeError):
    print("Wrong config file or path. ")


ea = EmailAlert(config_json['email'])
ea.send_email('test')

cf = CFLOG(config_json['cf'], ea)
