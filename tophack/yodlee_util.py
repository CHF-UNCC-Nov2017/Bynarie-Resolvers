"""A small collection of utilities for accessing the Yodlee API - yodlee cobrand information should be put in
cobrandinfo.json in the working directory. """

import json
from collections import ChainMap

import requests


class Api:
    """Very simple wrapper for the Yodlee api - allows for multiple instances which use different base urls,
    and get/post requests on various endpoints. This leaves out some of the needed endpoints, like put/delete
    requests, but for the purposes of the hackathon it works well. """
    base_headers = {
        "Accept": "application/json",
        "User-Agent": "TopHack Contestants group 3",
        "Accept-Language": "en-US"
    }

    def __init__(self, baseurl):
        self.baseurl = baseurl

    def get(self, endpoint, session=None, params=None):
        """
        :param session: A Session object with cobrand and user session tokens, or None if no authorization
        :return: JSON parsed response as a dict
        """

        headers = Api.base_headers
        if session:
            headers = ChainMap(session.auth, Api.base_headers)

        # possible failure if get fails; like if bad authorization. Return None or raw text? raise error?
        return requests.get(self.baseurl + endpoint, params=params or {}, headers=headers).json()

    def post(self, endpoint, data, session=None, **kwargs):
        """
        :param session: A Session object with cobrand and user session tokens, or None if no authorization
        :param kwargs: Any additional arguments are added into the post data with a ChainMap
        :return: JSON parsed response as a dict
        """
        headers = Api.base_headers
        if session:
            headers = ChainMap(session.auth, Api.base_headers)

        data = dict(ChainMap(kwargs, data))

        # possible failure if get fails; like if bad authorization. Return None or raw text? raise error?
        return requests.post(self.baseurl + endpoint, data=data, headers=headers).json()

    def delete(self, endpoint, session=None):
        headers = Api.base_headers
        if session:
            headers = ChainMap(session.auth, Api.base_headers)

        requests.delete(self.baseurl + endpoint, headers=headers)


# common yodlee apis, most useful for our data scraping and query tests during the hackathon
auth_api = Api('https://rest.developer.yodlee.com/services/srest/restserver/v1.0')
user_api = Api('https://developer.Api.yodlee.com/ysl')
cob_token = None


def get_cob_token():
    """Gets a static cobrand token for these queries. This should be updated with a more robust and persistent
    system, but it works well for these scripts """
    # probably should use some sort of singleton or factory pattern to manage queries on user data in actual
    # implementation - but, for small scale, a module global works well
    global cob_token

    if not cob_token:
        with open('cobrandinfo.json') as f:
            cobdata = json.load(f)

        cob_sess = auth_api.post('/authenticate/coblogin', data=cobdata)
        cob_token = cob_sess['cobrandConversationCredentials']['sessionToken']

    return cob_token


class Session:
    """Basic user-cobrand session manager; pulls authorization tokens from user login request"""

    def __init__(self, data):
        self.login_name = data['loginName']
        self.cob_token = data['userContext']['cobrandConversationCredentials']['sessionToken']
        self.user_token = data['userContext']['conversationCredentials']['sessionToken']

    @property
    def auth(self):
        return dict(
            Authorization=f'{{cobSession={self.cob_token},userSession={self.user_token}}}'
        )

    @staticmethod
    def login(login, password):
        user_sess = auth_api.post('/authenticate/login', data=dict(
            login=login,
            password=password,
            cobSessionToken=get_cob_token()
        ))

        return Session(user_sess)
