#!/usr/bin/env python3

import argparse
import json
import smtplib
import os
from cloudfoundry_client.client import CloudFoundryClient
from email.message import EmailMessage


DEFAULT_CONFIG = 'config.json'

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-c", "--config", help="config file. Example: config.json", type=str, default=DEFAULT_CONFIG)

args = parser.parse_args()


class alert():

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


class cflog():

    def __init__(self, cred, mail, proxy):

        client = CloudFoundryClient(cred['api'], proxy=proxy)

        client.init_with_user_credentials(cred['user'], cred['password'])

        org = client.v2.organizations.get_first(**{'name': cred['org']})
        org_guid = org['metadata']['guid']

        space = client.v2.spaces.get_first(**{'name': cred['space']})
        space_guid = space['metadata']['guid']

        for app in client.v2.apps.list(space_guid=space_guid):
            for log in app.recent_logs():
                print(log)


if __name__ == "__main__":

    try:
        with open(args.config, 'r') as json_file:
            config_json = json.load(json_file)
    except (FileNotFoundError, IOError, json.decoder.JSONDecodeError):
        print("Wrong config filename or path.")

    ea = alert(config_json['email'])

    http_proxy = os.environ.get('HTTP_PROXY', '')
    https_proxy = os.environ.get('HTTPS_PROXY', '')

    proxy = dict(http=http_proxy, https=https_proxy)
    cf = cflog(config_json['cf'], ea, proxy)
