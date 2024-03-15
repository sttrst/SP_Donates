from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.template import Context, loader
from django.db import models
from .models import StreamerUser
import requests
import pyspapi
import base64
from django.views.decorators.csrf import csrf_exempt



# Create your views here.

auth_url_ds = ""
spapi = pyspapi.SPAPI(card_id='', token='')


def mainp(request: HttpRequest):
    return render(request, 'index.html')


def home(request: HttpRequest) -> JsonResponse:
    return JsonResponse({"msg": "Hello World!"})


def render_a_donates(request: HttpRequest):
    return render(request, 'donate_show.html')


@csrf_exempt
def webhook_receiver(request):
    data = request.POST.get('data', '')
    return render(request, 'donate_show.html', {'data': data})


@login_required(login_url="/oauth2/login")
def get_authenticated_user(request: HttpRequest):
    print('ENTERING /AUTH/USER WITH USER DICT:', request.user)
    user = request.user

    if len(request.GET.keys()) == 0:
        print('NO PARAM ENTER TO /AUTH/USER')
        return redirect(f"/auth/user?idl={user.id}")

    mcun = spapi.get_user(user.id).username
    mcuuid = pyspapi.MojangAPI.get_uuid(username=mcun)
    mc_skin = pyspapi.MojangAPI.get_profile(uuid=mcuuid).skin_url

    idl = request.GET.get('idl')

    if StreamerUser.objects.filter(id=user.id).exists():
        a = open_stream_link(user, idl)
        if a == 'p':
            return render(request, 'profile_streamer.html', {'mcname': mcun, 'dsid': user.id, 'mcskin': mc_skin})
        else:
            smcun = spapi.get_user(idl).username
            smcuuid = pyspapi.MojangAPI.get_uuid(username=smcun)
            smc_skin = pyspapi.MojangAPI.get_profile(uuid=smcuuid).skin_url
            if request.method == 'POST':
                my_input_text = request.POST.get('myInputText', '')
                my_input_summ = request.POST.get('myInputSumm', '')
                return redirect(spapi.payment(amount=my_input_summ,
                                              redirect_url=f'http://91.186.199.207/auth/user?idl={user.id}',
                                              #webhook_url=f'http://91.186.199.207/donates?idl={idl}',
                                              webhook_url=f'http://91.186.199.207/webhook',
                                              data=my_input_text
                                              ))
                # return HttpResponse(f"user  задонатил {my_input_summ} АР(-ов)"
                #                     f" со словами {my_input_text}")
            else:
                return render(request, 'profile_streamer_donate.html',
                              {'mcname': smcun, 'dsid': idl, 'mcskin': smc_skin})

    elif request.method == 'POST':
        my_input_summ = request.POST.get('myInputSumm', '')
        if len(str(my_input_summ)) == 5:
            form = StreamerUser.objects.create(id=user.id, twitch_url=f'not_a_TTWU_{mcun}',
                                               card_num=my_input_summ,
                                               balance=0,
                                               unic_link=unic_link_gen(mcun, int(my_input_summ)),
                                               min_donate=1)
            a = open_stream_link(user, idl)
            if a == 'p':
                return render(request, 'profile_streamer.html', {'mcname': mcun, 'dsid': user.id, 'mcskin': mc_skin})
            else:
                smcun = spapi.get_user(idl).username
                smcuuid = pyspapi.MojangAPI.get_uuid(username=smcun)
                smc_skin = pyspapi.MojangAPI.get_profile(uuid=smcuuid).skin_url
                return render(request, 'profile_streamer_donate.html',
                              {'mcname': smcun, 'dsid': idl, 'mcskin': smc_skin})
        else:
            return render(request, 'profile_error.html', {'mcname': mcun, 'dsid': user.id, 'mcskin': mc_skin})
    return render(request, 'profile.html', {'mcname': mcun, 'dsid': user.id, 'mcskin': mc_skin})


def open_stream_link(user, idl):
    if int(idl) == int(user.id):
        print('PARAM.ID EQUELS USER.ID')
        return 'p'
    elif StreamerUser.objects.filter(id=idl).exists():
        print('PARAM.ID IS IN STREAMER DB')
        if int(idl) == int(user.id):
            print('PARAM.ID EQUELS USER.ID')
            return 'p'
        else:
            print('PARAM.ID not EQUELS USER.ID')
            return 's'
    else:
        print('PARAM.ID IS not IN STREAMER DB')
        return 'p'


def rend_aust(request, user):
    id = request.GET.get('id')


def authenticated_user_streamers(request: HttpRequest):
    return render(request, 'streamers.html')


def input_view(request):
    if request.method == 'POST':
        my_input_text = request.POST.get('myInputText', '')
        my_input_summ = request.POST.get('myInputSumm', '')
        return HttpResponse(f"user  задонатил {my_input_summ} АР(-ов)"
                            f" со словами {my_input_text}")
    else:
        return render(request, 'main.html')


def ds_login(request: HttpRequest):
    return redirect(auth_url_ds)


def ds_login_redirect(request: HttpRequest):
    code = request.GET.get('code')
    print('ENTERING DS/LOGIN/REDIRECT WITH CODE:', code)
    user = exc_code(code)
    discord_user = authenticate(request, user=user)
    discord_user = list(discord_user).pop()
    print('GOT A DS USER:', discord_user)
    login(request, discord_user)
    # return JsonResponse({"user": user})
    return redirect(f"/auth/user?idl={user['id']}")


def exc_code(code: str):
    data = {
        "client_id": "1197992619284910110",
        "client_secret": "aRIPh7V3eVP5PeyZt9iogQFM_l-7nZVO",
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "http://localhost:8000/oauth2/login/redirect",
        "scope": "identify"
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.post("https://discord.com/api/oauth2/token", data=data, headers=headers)
    credentials = response.json()
    access_token = credentials['access_token']
    response = requests.get("https://discord.com/api/v6/users/@me", headers={
        'Authorization': 'Bearer %s' % access_token
    })
    user = response.json()
    print('GOT USER IN EXC-CODE:', user)
    return user


def unic_link_gen(li, cn):
    cn = hex(cn)[2:]
    lo = ''
    for y in [hex(ord(x))[2:] for x in li]:
        lo += y
    lo = f'{lo}{cn}'
    return lo
