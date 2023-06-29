import random


def su_cut(string, len_string):
    if len(string) > len_string:
        string = string[0:len_string]
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
