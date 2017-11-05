"""First test to use the yodlee api - also used this file to put together a prototype for the contents of
yodlee_util.py """

import json

from scripts import api

with open('cobrandinfo.json') as f:
    cobdata = json.load(f)

with open('userinfo.json') as f:
    userdata = json.load(f)

if __name__ == '__main__':
    cobSes = api.yodleeAuth.post('/authenticate/coblogin', data=cobdata)
    cobSesToken = cobSes['cobrandConversationCredentials']['sessionToken']

    users = []

    for user in userdata:
        userSes = api.yodleeAuth.post('/authenticate/login', data=user, cobSessionToken=cobSesToken)
        userConvoToken = userSes['userContext']['conversationCredentials']['sessionToken']

        authHeader = {'Authorization': f'{{cobSession={cobSesToken},userSession={userConvoToken}}}'}

        useraccts = api.yodleeUser.get('/restserver/v1/accounts', extraheaders=authHeader)
        users.append(useraccts)

        userSes = api.yodleeAuth.post('/jsonsdk/Login/logout', data={
            'cobSessionToken': cobSesToken,
            'userSessionToken': userConvoToken
        }, cobSessionToken=cobSesToken)

    with open('users.json', 'w') as f:
        json.dump(users, f)
