from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect,\
    HttpResponseServerError, HttpResponseBadRequest, JsonResponse
from .models import Guest, PrivateChat, PrivateMessage, GuestSession
from django.template import loader
from django.urls import reverse
import random
import time
import json
import hashlib


from .views_helper import su_cut, generate_random_key, set_default_if_empty,\
    get_bool_value_from_request, anti_ddos, anti_ddos_decorator, my_hash


def openaccount(request):
    try:
        user_name = su_cut(request.COOKIES['matmech_user_name'], 100)
        session_key = su_cut(request.COOKIES['matmech_session_key'], 100)
        user = Guest.objects.get(name=user_name)

        if len(GuestSession.objects.filter(session_key=session_key, guest=user)) == 0:
            user_name = 'default'
            user = Guest.objects.get(name=user_name)
    except:
        user_id = 1
        user = Guest.objects.get(id=1)
    return user


def login(request):
    if request.method == 'POST':
        guest_name = su_cut(request.POST['name'], 100)
        guest_hashed_password = my_hash(su_cut(request.POST['password'], 100))
        if (len(Guest.objects.filter(name=guest_name))) == 0:
            return JsonResponse({'result': 'error', 'information': 'account not found'})
        else:
            this_user = Guest.objects.get(name=guest_name)
            if this_user.hashed_password == guest_hashed_password:
                try:
                    http_user_agent = su_cut(request.META['HTTP_USER_AGENT'], 500)
                except:
                    http_user_agent = 'no informations'
                session_key = generate_random_key(50)
                new_session_for_user = GuestSession(guest=this_user,
                                                    session_key=session_key, http_user_agent=http_user_agent)
                new_session_for_user.save()
                context = {
                    'result': 'success',
                    'user_id': this_user.id,
                    'session_key': session_key,
                    'user_name': guest_name,
                }
                return JsonResponse(context)
            else:
                return JsonResponse({'result': 'error', 'information': 'password incorrect'})
    else:
        return JsonResponse({'result': 'error', 'information': 'request must be post'})


def registration(request):
    if request.method == 'POST':
        guest_name = su_cut(request.POST['name'], 100)
        guest_hashed_password = my_hash(su_cut(request.POST['password'], 100))
        about = su_cut(request.POST['about'], 5000)
        pub_date = timezone.now()
        if (len(Guest.objects.filter(name=guest_name))) == 1:
            return JsonResponse({'result': 'error', 'information': 'name reserved'})
        else:
            new_user = Guest(name=guest_name, hashed_password=guest_hashed_password,
                             about=about, pub_date=pub_date)
            try:
                http_user_agent = su_cut(request.META['HTTP_USER_AGENT'], 500)
            except:
                http_user_agent = 'no informations'
            session_key = generate_random_key(50)
            new_session_for_user = GuestSession(guest=new_user,
                                                session_key=session_key, http_user_agent=http_user_agent)
            new_session_for_user.save()
            context = {
                'result': 'success',
                'user_id': new_user.id,
                'session_key': session_key,
                'user_name': guest_name,
            }
            return JsonResponse(context)
    else:
        return JsonResponse({'result': 'error', 'information': 'request must be post'})


def main(request):
    json_result = {"text": "hi on our website"}
    return JsonResponse(json_result)


def my_account(request):
    user = openaccount(request)
    template = loader.get_template('physicsesc/user.html')
    chats_count = len(user.task_set.all())
    context = {
        'tasks_count': chats_count,
        'user': user,
        'its_me': True,
        'color_theme': user.color_theme,
    }
    return HttpResponse(template.render(context, request))


def my_chats(request):
    return HttpResponseRedirect("matmech/chats/private/")
    user = openaccount(request)
    print(dir(user))
    private_chats = json.dumps(user.privatechat_set.all())
    return JsonResponse(private_chats)


def private_chats(request):
    user = openaccount(request)
    chats_list = user.privatechat_set.all()
    result_chats_list = list()
    for chat in chats_list:
        chat.other_author = chat.authors.exclude(id=user.id)[0]
        if chat.authors.all()[0] == user:
            chat.not_checked_messages = chat.author_1_not_checked_messages_count
            chat.author_0_not_checked_messages_count = 0
        else:
            chat.not_checked_messages = chat.author_2_not_checked_messages_count
            chat.author_1_not_checked_messages_count = 0

        if len(chat.privatemessage_set.all()) > 0:
            chat.last_message = chat.privatemessage_set.all()[len(chat.privatemessage_set.all()) - 1]
        else:
            chat.last_message = "история общения пуста"
        result_chats_list.append({'other_author_name': chat.other_author.name,
                                  'not_checked_messages': chat.not_checked_messages,
                                  'last_message': chat.last_message
                                  })
    context = {
        'chats_list': result_chats_list,
        'user':
        {
            'name': user.name,
            'hashed_password': user.hashed_password,
        }
    }
    return JsonResponse(context)



def account(request, guest_id):
    return HttpResponse("ggg")


def private_chat(request, guest_id):
    return HttpResponse("ggg")


def send_message(request, guest_id):
    return HttpResponse("ggg")