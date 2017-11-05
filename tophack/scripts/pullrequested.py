"""Small script to pull account data for teammates to look at to find good ways to classify users"""

import json

from collections import defaultdict

with open('userdata.json') as f:
    alldata = json.load(f)

if __name__ == '__main__':
    accts = []
    acct_keys = [
        'CONTAINER',
        'providerAccountId',
        'accountName',
        'accountType',
        'id',
        'balance',
        'accountNumber',
        'availableBalance',
        'availableCash',
        'availableCredit',
        'totalCreditLine',
        'providerId',
        'providerName',
        'overDraftLimit',
    ]

    for user in alldata:
        for acct in user['accounts']['account']:
            acct = defaultdict(str, acct)
            smaller = {
                k: acct[k] for k in acct_keys
            }
            accts.append(smaller)
    with open('requested_accounts.json', 'w') as f:
        json.dump(accts, f)

