#!/usr/bin/env python3

import argparse
import json
import cfmail
import os
from threading import Thread

from cloudfoundry_client.client import CloudFoundryClient


def streamer(app, conf):
    """ app log streams """

    name = app['entity']['name']

    print("[{}] Starting log check.".format(name))

    for log in app.stream_logs():
        print("[{}] {}".format(name, log))
        for key in conf['keys']:
            if key.lower() in str(log).lower():
                print("[{}] Found key: {}!!".format(name, key))

                body = "Org/space: {}/{}\n".format(conf['cf']['org'], conf['cf']['space'])
                body = "{}App: {}\nKey: {}\nLog: {}\n".format(body, name, key, log)

                cfmail.mail(body, conf['email'])


def get_args():
    """ Get args"""

    default_config = 'config.json'
    default_proxy = ''

    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("-c", "--config", help="config file. Example: config.json", type=str, default=default_config)
    parser.add_argument("-p", "--proxy", help="HTTPS proxy.", type=str, default=default_proxy)

    return parser.parse_args()


def get_config(config):
    """ parse config file """
    try:
        with open(config, 'r') as json_file:
            return json.load(json_file)
    except (FileNotFoundError, IOError, json.decoder.JSONDecodeError):
        print("Wrong config filename or path.")


def get_proxy(proxy):
    """ proxy setup """
    if proxy == '':
        http_proxy = os.environ.get('HTTP_PROXY', '')
        https_proxy = os.environ.get('HTTPS_PROXY', '')
    else:
        http_proxy = proxy
        https_proxy = proxy

    return dict(http=http_proxy, https=https_proxy)


def cf_login(cf, proxy):
    """ cf login """
    client = CloudFoundryClient(cf['api'], proxy=proxy)
    client.init_with_user_credentials(cf['user'], cf['password'])

    return client


def get_space_guid(name):
    """ Get space guid """
    space = client.v2.spaces.get_first(**{'name': name})

    return space['metadata']['guid']


def get_org_guid(name):
    """ Get org guid """
    org = client.v2.organizations.get_first(**{'name': name})

    return org['metadata']['guid']


if __name__ == "__main__":

    args = get_args()

    config_json = get_config(args.config)

    proxy = get_proxy(args.proxy)
    client = cf_login(config_json['cf'], proxy)

    org_guid = get_org_guid(config_json['cf']['org'])
    space_guid = get_space_guid(config_json['cf']['space'])

    threads = []
    for app in client.v2.apps.list(space_guid=space_guid):
        t = Thread(target=streamer, args=(app, config_json,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
