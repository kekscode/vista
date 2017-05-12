#!/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import logging
import json
import requests
from urlparse import urljoin

logging.basicConfig(level=logging.ERROR, format="%(asctime)s;%(levelname)s;%(message)s")
logger = logging.getLogger(sys.argv[0])

class CheckvistUserAccount:
    def __init__(self, username, remote_key):
        self.username = username
        self.remote_key = remote_key

        self.base_url = 'https://checkvist.com'
        self.auth_url = urljoin(self.base_url, '/auth/login.json?username={0}&remote_key={1}'.format(self.username, self.remote_key))

    def authenticate(self):
        r = requests.post(self.auth_url, {'username': self.username, 'remote_key': self.remote_key})
        if r.status_code == 200:
           self.api_token = r.text.replace('"', '').strip()
           return True
        else:
            logger.error(r.content)
            return False

def main():
    def get_env():
        user = 'CHECKVIST_USERNAME'
        key  = 'CHECKVIST_REMOTE_KEY'
        if os.getenv(user, default=None) and os.getenv(key, default=None):
            username = os.getenv(user)
            remote_key = os.getenv(key)
        else:
            logger.error("Either {0} or {1} environment variable is empty".format(user, key))
            sys.exit(1)
        return user, key

    username, remote_key = get_env()
    cv = CheckvistUserAccount(username, remote_key)
    if not cv.authenticate():
        logger.error("Could not authenticate with checkvist.com")

if __name__ == '__main__':
    main()
