import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse

import mockup.util.userinfo as userinfo

from mockup.models import Profile


def user_dashboard(request):
    prof = request.user.profile  # type:Profile

    selected_options = json.loads(prof.options)

    data = dict(
        accounts=[],
        transactions=[],
        holdings=[],
        statements=[],
        networth=[]
    )

    if prof.yodlee_login and prof.yodlee_password:
        info = userinfo.get_user_info(prof.yodlee_login, prof.yodlee_password, selected_options)

        for acc in info.get('accounts', {}).get('account', []):
            data['accounts'].append(dict(
                name=acc['accountName'],
                provider=acc['providerName'],
                type=acc['accountType']
            ))

        for st in info.get('statements', {}).get('statement', []):
            data['statements'].append(dict(
                payment=st['lastPaymentAmount']['amount'],
                paymentCurrency=st['lastPaymentAmount']['currency'],
                date=st['statementDate']
            ))

        for entry in info.get('networth', {}).get('networth', []):
            data['networth'].append(dict(
                date=entry['date'],
                networth=entry['networth']['amount'],
                currency=entry['networth']['currency']
            ))

    return render(request, 'mockup/userdashboard.html', context=dict(
        user=request.user,
        data=data,
        all_options=userinfo.all_options,
        selected_options=selected_options
    ))


def superuser_dashboard(request):
    other_users = User.objects.all().filter(profile__is_customer=True)

    users_data = []

    for usr in other_users:
        options = json.loads(usr.profile.options)
        info = userinfo.get_user_info(usr.profile.yodlee_login, usr.profile.yodlee_password, options)
        data = {
            option: info[option] for option in options
        }
        users_data.append(dict(
            raw_info=json.dumps(info),
            options=options,
            data=data
        ))

    return render(request, 'mockup/superuserdashboard.html', context=dict(
        user=request.user,
        users_data=users_data
    ))


@login_required
def detail(request):
    if not request.user.is_authenticated:
        return redirect(index)

    if 'option' in request.POST:
        options = [option for option in userinfo.all_options if option in request.POST]

        prof = request.user.profile
        prof.options = json.dumps(options)
        prof.save()

        return HttpResponseRedirect(reverse('mockup:dash'))

    if request.user.is_superuser:
        return superuser_dashboard(request)

    return user_dashboard(request)


def index(request):
    return render(request, 'mockup/index.html')
