import random
import time
from django.http import HttpResponse, HttpResponseRedirect,\
    HttpResponseServerError, HttpResponseBadRequest


def su_cut(string, string_length):
    if len(string) > string_length:
        string = string[0:string_length]
    return string


def generate_random_key(key_length=50):
    s = "1234567890" \
        "abcdefghijklmnopqrstuvwxyz" \
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ" \
        "абвгдежзийклмнопрстуфхцчшщъыьэюя" \
        "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    session_key = ""
    for j in range(key_length):
        session_key += s[random.randint(0, 125)]
    return session_key


def set_default_if_empty(variable, default):
    if variable in [[], "", " ", "  "]:
        return default
    return variable


def get_bool_value_from_request(request, value_name):
    value_type_private = False
    try:
        if request.POST[value_name]:
            value_type_private = True
        else:
            value_type_private = False
    except:
        value_type_private = False
    return value_type_private


massive_of_users = dict()
requests_count = 0


def anti_ddos(request):
    print(time.time())
    global massive_of_users
    user_ip = request.META['REMOTE_ADDR']
    if user_ip in massive_of_users:
        if len(massive_of_users[user_ip]) < 2:
            massive_of_users[user_ip].append(time.time())
            return True
        if massive_of_users[user_ip][0] + 0.7 < time.time():
            massive_of_users[user_ip][0] = time.time()
            return True
        elif massive_of_users[user_ip][1] + 0.7 < time.time():
            massive_of_users[user_ip][1] = time.time()
            return True
        return False
    else:
        massive_of_users[user_ip] = [time.time()]
        return True


def calculate_request():
    global requests_count
    if requests_count % 1000 == 0:
        #create()
        #restart_top_of_rooms()
        pass
    requests_count += 1


def anti_ddos_decorator(func):
    def new_func(request, *args, **kwargs):
        calculate_request()
        if anti_ddos(request):
            return func(request, *args, **kwargs)
        else:
            return HttpResponseServerError()
            # return HttpResponse("sorry, it seems it a ddos attack")

    new_func.__doc__ = func.__doc__
    new_func.__name__ = func.__name__
    return new_func


def my_hash(string):
    s = "1234567890" \
        "abcdefghijklmnopqrstuvwxyz" \
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ" \
        "абвгдежзийклмнопрстуфхцчшщъыьэюя" \
        "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    result_hash = 0
    for letter in string:
        result_hash *= 7
        if letter in s:
            result_hash += s.index(letter)
        else:
            result_hash += 1
    result_hash %= 2**20
