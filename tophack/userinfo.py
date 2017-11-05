import json
from pprint import pprint

import datetime

from yodlee_util import user_api, Session
import yodlee_util as yodlee


def days_ago(n=30):
    return (datetime.datetime.now() - datetime.timedelta(-n)).isoformat()


option_queries = {
    'accounts':  # get information from this user of all accounts they have linked
        lambda session: user_api.get('/restserver/v1/accounts', session=session),

    'transactions1mo':  # get 30 days transacation history
        lambda session: user_api.get('/restserver/v1/transactions', session=session,
                                     params=dict(fromDate=days_ago(30))),

    'transactions3mo':  # get 90 days transaction history
        lambda session: user_api.get('/restserver/v1/transactions', session=session,
                                     params=dict(fromDate=days_ago(90))),

    'holdings':  # get holdings information from this user of accounts they have linked
        lambda session: user_api.get('/restserver/v1/holdings', session=session),

    'statements':  # get active statements from this user
        lambda session: user_api.get('/restserver/v1/statements', session=session),

    'networth':  # get net worth from this user
        lambda session: user_api.get('/restserver/v1/derived/networth', session=session),
}


def get_user_info(login, password, options=()):
    """
    Get user info - query our database and get the yodlee credentials and information sale options of this user
    :param options: a sequence of str for options to use. may be any key of option_queries.
    """
    u_sess = Session.login(login, password)

    data = {}

    for option in options:
        if option in option_queries:
            data[option] = option_queries[option](u_sess)
        else:
            data[option] = {'Error': 'No such option'}

    user_api.get('/restserver/v1/user/logout', session=u_sess)

    return data


if __name__ == '__main__':
    with open('userinfo.json') as f:
        ui = json.load(f)

    user_info = get_user_info(**ui[0], options=['accounts', 'holdings', 'networth'])

    pprint(user_info)
