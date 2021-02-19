#!/usr/bin/env python3

import json
import smtplib
from email.message import EmailMessage


def mail(message, conf):

    subject = f'CF log alert'

    msg = EmailMessage()
    msg.set_content(message)

    msg['Subject'] = subject
    msg['From'] = conf['sender_email']
    msg['To'] = conf['receiver_email']

    with smtplib.SMTP(conf['smtp'], conf['port']) as m:
        m.send_message(msg)


if __name__ == "__main__":
    pass
