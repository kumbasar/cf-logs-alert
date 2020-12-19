#!/usr/bin/env python3

import argparse
import json
import smtplib


DEFAULT_CONFIG = 'config.json'

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-c", "--config", help="Set config file. Example: config.json", type=str, default=DEFAULT_CONFIG)

args = parser.parse_args()

config_json = ''

try:
    with open(args.config, 'r') as json_file:
        config_json = json.load(json_file)
except (FileNotFoundError, IOError, json.decoder.JSONDecodeError):
    print("Wrong config file or path. ")

print(config_json)

