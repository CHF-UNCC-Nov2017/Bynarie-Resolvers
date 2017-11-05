"""
Basic user scraping script - mostly a test to see what kinds of data we can get from users.
"""


import json

from scripts import api

with open('cobrandinfo.json') as f:
    cobdata = json.load(f)

with open('userinfo.json') as f:
    userinfos = json.load(f)

if __name__ == '__main__':
    all_users = []

    for user in userinfos:
        cobSes = api.yodleeAuth.post('/authenticate/coblogin', data=cobdata)
        cobSesToken = cobSes['cobrandConversationCredentials']['sessionToken']

        endpoints = [
            '/restserver/v1/accounts',
            '/restserver/v1/accounts/historicalBalances',
            '/restserver/v1/holdings',
            '/restserver/v1/transactions',
            '/restserver/v1/statements',
            # todo: get transaction summary separately
            # ('/restserver/v1/derived/transactionSummary', {'groupBy': 'CATEGORY'}),
            '/restserver/v1/derived/networth',
        ]

        userSes = api.yodleeAuth.post('/authenticate/login', data=user, cobSessionToken=cobSesToken)
        userConvoToken = userSes['userContext']['conversationCredentials']['sessionToken']

        print('userSes', userSes)

        authHeader = {'Authorization': f'{{cobSession={cobSesToken},userSession={userConvoToken}}}'}

        user_dict = {}

        print('user', user['login'])
        for endpoint in endpoints:
            params = {}
            if isinstance(endpoint, tuple):
                endpoint, params = endpoint
            name = endpoint[15:]
            data = api.yodleeUser.get(endpoint, params=params, extraheaders=authHeader)
            user_dict[name] = data
            print('done', name)

        all_users.append(user_dict)

    with open('userdata.json', 'w') as f:
        json.dump(all_users, f)
