"""Prototype class for yodlee_util.py - used in most of this directory for simple scripts to test the yodlee sandbox
environment """

from collections import ChainMap

import requests


class Api:
    baseheaders = {
        "Accept": "application/json",
        "User-Agent": "tophack hackathon contestents group 3",
        "Accept-Language": "en-US"
    }

    def __init__(self, baseurl):
        self.baseurl = baseurl

    def get(self, endpoint, extraheaders=None, params=None):
        headers = ChainMap(extraheaders or {}, Api.baseheaders)

        return requests.get(self.baseurl + endpoint, headers=headers, params=params or {}).json()

    def post(self, endpoint, data, extraheaders=None, **kwargs):
        headers = ChainMap(extraheaders or {}, Api.baseheaders)

        data = dict(ChainMap(kwargs, data))

        base_endpoint = self.baseurl + endpoint
        return requests.post(base_endpoint, data=data, headers=headers).json()


yodleeAuth = Api('https://rest.developer.yodlee.com/services/srest/restserver/v1.0')

yodleeUser = Api('https://developer.Api.yodlee.com/ysl')
