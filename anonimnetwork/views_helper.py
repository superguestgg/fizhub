import random


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


class Links:
    main_page = "<a href='/anonnetwork/main'>main page</a><br>"
    bug_report = "<a href='/anonnetwork/admin'>bug report</a><br>"

    @staticmethod
    def room(room_name):
        return f"<a href='/anonnetwork/{room_name}'>перейти к комнате</a><br>"

    @staticmethod
    def message(room_name, message_id):
        return f"<a href='/anonnetwork/{room_name}/{message_id}'>current message</a><br>"
