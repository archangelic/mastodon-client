#!/usr/bin/env python3
from getpass import getpass
import json
from os import chmod, environ, mkdir, path

import click
from mastodon import Mastodon


# function to set everything up
def setup(set_dir):
    api_url = input("Enter your instance URL: ")
    user = input("Enter your email address: ")
    pw = getpass("Password: ")
    client_id, client_secret = Mastodon.create_app('tilde.toot', api_base_url=api_url)
    mastodon = Mastodon(client_id=client_id, client_secret=client_secret, api_base_url=api_url)
    access_token = mastodon.log_in(user, pw)
    m = {
        'client_id': client_id,
        'client_secret': client_secret,
        'api_base_url': api_url,
        'access_token': access_token
    }
    with open(set_dir, 'w') as json_data:
        json.dump(m, json_data)

@click.command()
@click.argument('toot_text')
def toot(toot_text):
    mastodon.toot(toot_text)

if __name__ == '__main__':
    # Checking and loading the settings file
    home = environ['HOME']
    tootdir = path.join(home, '.toot')
    if not path.isdir(tootdir):
        mkdir(tootdir)
    set_file = path.join(tootdir, 'settings.json')
    if not path.exists(set_file):
        open(set_file, 'w').close()
        chmod(set_file, 0o600)
        setup(set_file)

    # Set up the client
    with open(set_file) as json_data:
        m = json.load(json_data)
    mastodon = Mastodon(
        client_id=m['client_id'],
        client_secret=m['client_secret'],
        api_base_url=m['api_base_url'],
        access_token=m['access_token']
    )

    # TOOT!
    toot()
