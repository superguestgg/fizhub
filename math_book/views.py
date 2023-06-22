from django.shortcuts import render, get_object_or_404
# from django.http import Http404
from django.conf import settings
from django.core.files.storage import FileSystemStorage
# from django.
from django.utils import timezone
# from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from .models import Subject, University, Ticket, Guest,\
    Session, Guest_session, Vote_ticket, Theorem, Vote_theorem, \
    Definition, Vote_definition, SessionTicket
from django.template import loader
from django.db.models import Q
from django.urls import reverse
import random

from .search_tree import NameTree


def set_default_if_empty(variable, default):
    if variable in [[], "", " ", "  "]:
        return default
    return variable


def generate_item_enters(item_str):
    item_str = item_str.split("\n")
    generated_item_str = ""
    for item_str_1 in item_str:
        generated_item_str += item_str_1+" (enter) "
    return generated_item_str


def get_bool_value_from_user(request, value_name):
    value_type_private = False
    try:
        if request.POST[value_name]:
            value_type_private = True
        else:
            value_type_private = False
    except:
        value_type_private = False
    return value_type_private


def return_error(request, error_link=False):
    error_text_list = ["server error", "sorry, it seems, it a server error",
                       "server error occured"]
    error_text = "<center>"+error_text_list[random.randint(0, 2)]+"</center>"
    error_text += "<br><a href='/math_book/'>main page</a>"
    if error_link:
        error_text += "<br><a href='"+error_link+"'>back</a>"
    return return_information(request, error_text, "exception", error_link)


def return_information(request, information_text, page_name_text="information", page_name_link=False):
    try:
        guest = open_account_guest(request)
        template = loader.get_template('math_book/information.html')
        context = {
            'information_text': information_text,
            'page_name_link': page_name_link,
            'page_name_text': page_name_text,
            'color_theme': guest.color_theme,
        }
        return HttpResponse(template.render(context, request))
    except:
        return HttpResponse('не ну этого не должно было произойти')


def su_cut(string, len_string):
    if len(string) > len_string:
        string = string[0:len_string]
    return string


def generate_random_key(key_length=50):
    s = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZабвгдежзийклмнопрстуфхцчшщъыьэюяАБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    session_key = ""
    for j in range(key_length):
        session_key += s[random.randint(0, 125)]
    return session_key


def generate_definitions_and_theorems(text):
    replaces = [["definition_link", "theorem_link"], [Definition, Theorem]]
    return generate_text_with_classes(text, replaces, "get_html")


def get_image_str(image_href):
    return "(enter) картинка по адресу (enter)<a href='" + image_href + "'>" \
           + image_href + "</a>(enter)" + \
           "<img scr='" + image_href + \
           "' alt='эй, тупо лох, пососи дуло(извини у меня такое было в наушниках)'>"


def generate_images(text):
    replaces = [["image_link"], [get_image_str]]
    return generate_text_without_classes(text, replaces)


def read_before_symbol(symbol, text, text_len, index_now):
    result = ""
    while index_now < text_len and text[index_now] != symbol:
        result += text[index_now]
        index_now += 1
    return (index_now, result)


def generate_text_without_classes(text, replaces=[["replace_word"], [str]]):
    text_len = len(text)
    verbnumber = 0
    while verbnumber < text_len:
        verbnumber = read_before_symbol("/", text, text_len, verbnumber)[0]
        if verbnumber >= text_len:
            break
        verbnumber_before_slesh = verbnumber
        verb = text[verbnumber]
        if verb == "/":
            replaces_index = -1
            # нахождение нужного для перезаписи элемента в replaces
            for i in range(len(replaces[0])):
                this_word_replace = replaces[0][i]
                this_word_replace_len = len(this_word_replace)
                if text[verbnumber + 1:verbnumber + 1 + this_word_replace_len] == this_word_replace:
                    replaces_index = i
                    break
            if replaces_index == -1:
                verbnumber += 1
                continue
            this_word = replaces[0][replaces_index]
            this_word_len = len(this_word)
            this_word_function = replaces[1][replaces_index]
            verbnumber += this_word_len

            verbnumber = read_before_symbol("'", text, text_len, verbnumber)[0]
            verbnumber += 1

            [verbnumber, i_cant_come_up_with_name] = read_before_symbol("'", text, text_len, verbnumber)
            verbnumber = read_before_symbol("/", text, text_len, verbnumber)[0]
            verbnumber += 1

            i_cant_come_up_with_name = str(i_cant_come_up_with_name)
            new_text = this_word_function(i_cant_come_up_with_name)
            length_of_new = len(new_text)
            text = text[:verbnumber_before_slesh] + new_text + text[verbnumber:]
            text_len = text_len - verbnumber + verbnumber_before_slesh + length_of_new
            verbnumber = verbnumber_before_slesh + length_of_new
        verbnumber += 1
    return text


def generate_text_with_classes(text, replaces=[["theorem_link"], [Theorem]], replace_function="get_html"):
    text_len = len(text)
    verbnumber = 0
    while verbnumber < text_len:
        verbnumber = read_before_symbol("/", text, text_len, verbnumber)[0]
        if verbnumber >= text_len:
            break
        verbnumber_before_slesh = verbnumber
        verb = text[verbnumber]
        if verb == "/":
            replaces_index = -1
            # нахождение нужного для перезаписи элемента в replaces
            for i in range(len(replaces[0])):
                this_word_replace = replaces[0][i]
                this_word_replace_len = len(this_word_replace)
                if text[verbnumber + 1:verbnumber + 1 + this_word_replace_len] == this_word_replace:
                    replaces_index = i
                    break
            if replaces_index == -1:
                verbnumber += 1
                continue
            this_word = replaces[0][replaces_index]
            this_word_len = len(this_word)
            this_class = replaces[1][replaces_index]
            verbnumber += this_word_len
            verbnumber = read_before_symbol("'", text, text_len, verbnumber)[0]
            verbnumber += 1
            [verbnumber, in_class_number] = read_before_symbol("'", text, text_len, verbnumber)
            verbnumber = read_before_symbol("/", text, text_len, verbnumber)[0]
            verbnumber += 1
            in_class_number = int(in_class_number)
            in_class = this_class.objects.get(id=in_class_number)
            function = getattr(this_class, replace_function)
            new_text = function(in_class)
            length_of_new = len(new_text)
            text = text[:verbnumber_before_slesh] + new_text + text[verbnumber:]
            text_len = text_len - verbnumber + verbnumber_before_slesh + length_of_new
            verbnumber = verbnumber_before_slesh + length_of_new
        verbnumber += 1
    return text


def open_account_guest(request):
    try:
        user_name = su_cut(request.COOKIES['math_book_user_name'], 40)
        session_key = su_cut(request.COOKIES['math_book_session_key'], 100)
        user = Guest.objects.get(guest_name=user_name)
        if len(Guest_session.objects.filter(session_key=session_key, guest=user)) == 0:
            # return HttpResponse('session inactive | user not found <br> сессия неактивна|пользователь не найден')
            user_name = 'undefined guest'
            user = Guest.objects.get(guest_name=user_name)
    except:
        user_name = 'undefined guest'
        user = Guest.objects.get(guest_name=user_name)
    return user


def sendaccountpost(request):
    if True:
        login_type = su_cut(request.POST['registration_type'], 50)
        guest_name = set_default_if_empty(su_cut(request.POST['guest_name'], 50), "no name")
        guest_password = su_cut(request.POST['guest_password'], 50)
        if login_type == "new":
            if (len(Guest.objects.filter(guest_name=guest_name))) == 0:
                try:
                    os = su_cut(request.META['OS'], 100)
                except:
                    os = 'no informations'
                try:
                    computername = su_cut(request.META['COMPUTERNAME'], 100)
                except:
                    computername = 'no informations'
                try:
                    HTTP_USER_AGENT = su_cut(request.META['HTTP_USER_AGENT'], 500)
                except:
                    HTTP_USER_AGENT = 'no informations'
                try:
                    guest_information = su_cut(request.POST['guest_information'], 2000)
                except:
                    return HttpResponse(
                        'аккаунт не обнаружен | account not found<br>or<br>guest_information not found | информация о пользователе не найдена')
                new_user = Guest(guest_name=guest_name, guest_password=guest_password,
                                 guest_information=guest_information)
                new_user.save()
                session_key = generate_random_key(50)
                new_session_for_user = Guest_session(guest=new_user, session_key=session_key, os=os,
                                                     computername=computername, HTTP_USER_AGENT=HTTP_USER_AGENT)
                new_session_for_user.save()
                template = loader.get_template('math_book/successfullyLogin.html')
                context = {
                    'user_id': new_user.id,
                    'session_key': session_key,
                    'user_name': guest_name,
                }
                return HttpResponse(template.render(context, request))
            else:
                return HttpResponse('имя занято | name reserved')
        else:
            if (len(Guest.objects.filter(guest_name=guest_name))) == 0:
                return HttpResponse('аккаунт не обнаружен | account not found<br>or<br>guest_information not found')
            else:
                this_user = Guest.objects.get(guest_name=guest_name)
                if this_user.guest_password == guest_password:
                    try:
                        os = su_cut(request.META['OS'], 100)
                    except:
                        os = 'no informations'
                    try:
                        computername = su_cut(request.META['COMPUTERNAME'], 100)
                    except:
                        computername = 'no informations'
                    try:
                        HTTP_USER_AGENT = su_cut(request.META['HTTP_USER_AGENT'], 500)
                    except:
                        HTTP_USER_AGENT = 'no informations'
                    session_key = generate_random_key(50)
                    new_session_for_user = Guest_session(guest=this_user, session_key=session_key, os=os,
                                                         computername=computername, HTTP_USER_AGENT=HTTP_USER_AGENT)
                    new_session_for_user.save()
                    template = loader.get_template('math_book/successfullyLogin.html')
                    context = {
                        'user_id': this_user.id,
                        'session_key': session_key,
                        'user_name': guest_name,
                    }
                    return HttpResponse(template.render(context, request))
                else:
                    return HttpResponse('name reserved|имя занято<br><a href="/physic-in-sesc/main">main page</a>')
    else:
        return HttpResponse("server error occurred")


def myaccount(request):
    if True:
        view_guest = open_account_guest(request)
        guest = view_guest

        template = loader.get_template('math_book/thisGuest.html')

        context = {
            'guest': guest,
            'page_name_text': guest.id,
            'color_theme': view_guest.color_theme,
            'is_me': True,
        }
        return HttpResponse(template.render(context, request))
    else:
        information_return = 'сессия недействительна'
        return return_information(request, information_return)


# auto
def get_guest(request, guest_id):
    try:
        view_guest = open_account_guest(request)
        guest = Guest.objects.get(id=guest_id)
        template = loader.get_template('math_book/thisGuest.html')
        context = {
            'guest': guest,
            'page_name_text': guest.id,
            'color_theme': view_guest.color_theme,
            'is_me': guest.id == view_guest.id,
        }
        return HttpResponse(template.render(context, request))
    except Guest.DoesNotExist:
        return HttpResponse('guest does not exist')
    except:
        return return_error(request)

def settings(request):
    try:
        guest = open_account_guest(request)
        if guest.guest_name == 'undefined guest':
            return HttpResponse('войдите сначала в свой аккаунт')
        template = loader.get_template('math_book/settings.html')
        sessions = guest.guest_session_set.all()
        session_key = su_cut(request.COOKIES['session_key'], 100)

        context = {
            'session_key': session_key,
            'page_name_text': 'настройки',
            'sessions': sessions,
            'guest': guest,
            'is_me': True,
            'color_theme': guest.color_theme,
        }

        return HttpResponse(template.render(context, request))
    except:
        information_return = 'сессия недействительна'
        return return_information(request, information_return)


def changecolortheme(request):
    try:
        user = open_account_guest(request)
        if user == "undefined guest":
            return HttpResponse('сессия недействительна')
        color_theme = su_cut(request.POST['color_theme'], 2000)
        if user.color_theme != color_theme:
            user.color_theme = color_theme
            user.save()
        return settings(request)
    except:
        return HttpResponse('сессия недействительна')


def closesession(request, session_key):
    try:
        user = open_account_guest(request)
        if len(user.guest_session_set.all().filter(session_key=session_key)) > 0:
            session = user.guest_session_set.all().get(session_key=session_key)
            session.delete()

        user = open_account_guest(request)
        template = loader.get_template('physicsesc/settings.html')
        sessions = user.guest_session_set.all()
        session_key = su_cut(request.COOKIES['session_key'], 100)
        context = {
            'session_key': session_key,
            'sessions': sessions,
            'user': user,
            'its_me': True,
            'color_theme': user.color_theme,

        }
        return HttpResponse(template.render(context, request))
    except:
        information_return = 'сессия недействительна'
        return return_information(request, information_return)


def changeaccountinformation(request):
    try:
        user = open_account_guest(request)
        if user == "undefined guest":
            information_return = 'сессия недействительна'
            return return_information(request, information_return)
        guest_information = su_cut(request.POST['guest_information'], 2000)
        if user.guest_information != guest_information:
            user.guest_information = guest_information
            user.save()
        return settings(request)
    except:
        information_return = 'сессия недействительна'
        return return_information(request, information_return)


def changepassword(request):
    try:
        user = open_account_guest(request)
        if user == "undefined guest":
            information_return = 'сессия недействительна'
            return return_information(request, information_return)
        old_password = su_cut(request.POST['old_password'], 40)
        new_password = su_cut(request.POST['new_password'], 40)
        if user.guest_password == old_password:
            user.guest_password = new_password
            user.save()
        return settings(request)
    except:
        information_return = 'сессия недействительна'
        return return_information(request, information_return)


def show_all_guest(request):
    return show_guest(request, 'all')


def show_guest(request, sort_type):
    return show_guest_page(request, sort_type, 1)


def show_guest_page(request, sort_type, page_number):
    try:
        guest = open_account_guest(request)
        page_number = max(1, page_number)
        if sort_type == "main":
            guests_list = Guest.objects.all()[(page_number - 1) * 50:page_number * 50]
        else:
            sort_type = 'main'
            guests_list = Guest.objects.all()[(page_number - 1) * 50:page_number * 50]
        page_count = len(Guest.objects.all()) // 50 + 1
        next_page = page_number < page_count
        template = loader.get_template('math_book/listGuest.html')
        context = {
            'guests_list': guests_list,
            'page_name_text': sort_type,
            'main_link': '/math_book/guests/' + sort_type,
            'pages': page_number,
            'pagescount': page_count,
            'next_page': next_page,
            'pagemenu': True,
            'color_theme': guest.color_theme,
        }
        return HttpResponse(template.render(context, request))
    except:
        return HttpResponse('error')


guest_search_tree = None


def first_search_guest():
    global guest_search_tree
    if guest_search_tree is None:
        guest_search_tree = NameTree(Guest, "ticket_count", "guest_name")
        guest_search_tree.create(Guest.objects.all())

def search_guest(request):
    # print(set(dir(Guest)) - set(dir(Guest_session)))
    global guest_search_tree
    first_search_guest()
    guest = open_account_guest(request)
    sort_type = 'search'

    if request.method == 'POST':
        string_search = request.POST['string_search']
        guests_list_id = guest_search_tree.search_with_mistakes(
            string_search, return_only_id=True)

        guests_list = Guest.objects.filter(id__in=guests_list_id)
        last_question = string_search
    else:
        guests_list = ""
        last_question = ""
    template = loader.get_template('math_book/searchGuest.html')
    context = {
        'last_question': last_question,
        'guests_list': guests_list,
        'page_name_text': 'поиск',
        'main_link': '/math_book/guests/' + sort_type,
        'pagemenu': True,
        'color_theme': guest.color_theme,
    }
    return HttpResponse(template.render(context, request))


def show_all_guest_sessions_from_guest(request, guest_id):
    return show_guest_sessions_from_guest(request, guest_id, 'all')


def show_guest_sessions_from_guest(request, guest_id, sort_type):
    return show_guest_sessions_from_guest_page(request, guest_id, sort_type, 1)


def show_guest_sessions_from_guest_page(request, guest_id, sort_type, page_number):
    try:
        view_guest = open_account_guest(request)
        guest = Guest.objects.get(pk=guest_id)
        guest_session_set = guest.guest_session_set.all()
        page_count = len(guest_session_set)
        next_page = page_number > page_count
        guest_sessions_list = guest.guest_session_set.all()[:100]
        template = loader.get_template('math_book/listGuest_session.html')
        context = {
            'guest_sessions_list': guest_sessions_list,
            'page_name_text': 'Guest guest_sessions',
            'main_link': '/math_book/guest/' + str(guest_id),
            'pages': page_number,
            'pagescount': page_count,
            'next_page': next_page,
            'pagemenu': True,
            'color_theme': view_guest.color_theme,
        }
        return HttpResponse(template.render(context, request))
    except:
        return return_error(request)


def show_all_tickets_from_guest(request, guest_id):
    return show_tickets_from_guest(request, guest_id, 'all')


def show_tickets_from_guest(request, guest_id, sort_type):
    return show_tickets_from_guest_page(request, guest_id, sort_type, 1)


def show_tickets_from_guest_page(request, guest_id, sort_type, page_number):
    try:
        guest = open_account_guest(request)
        guest = Guest.objects.get(pk=guest_id)
        ticket_set = guest.ticket_set.all()
        page_count = len(ticket_set)
        next_page = page_number > page_count
        tickets_list = guest.ticket_set.all()[:100]
        template = loader.get_template('math_book/listTicket.html')
        context = {
            'tickets_list': tickets_list,
            'page_name_text': 'Guest tickets',
            'main_link': '/math_book/guest/' + str(guest_id),
            'pages': page_number,
            'pagescount': page_count,
            'next_page': next_page,
            'pagemenu': True,
            'color_theme': guest.color_theme,
        }
        return HttpResponse(template.render(context, request))
    except:
        return return_error(request)



def show_all_sessions_from_guest(request, guest_id):
    return show_sessions_from_guest(request, guest_id, 'all')


def show_sessions_from_guest(request, guest_id, sort_type):
    return show_sessions_from_guest_page(request, guest_id, sort_type, 1)


def show_sessions_from_guest_page(request, guest_id, sort_type, page_number):
    try:
        guest = open_account_guest(request)
        guest = Guest.objects.get(pk=guest_id)
        session_set = guest.session_set.all()
        page_count = len(session_set)
        next_page = page_number > page_count
        sessions_list = guest.session_set.all()[:100]
        template = loader.get_template('math_book/listSession.html')
        context = {
            'sessions_list': sessions_list,
            'page_name_text': 'Guest sessions',
            'main_link': '/math_book/guest/' + str(guest_id),
            'pages': page_number,
            'pagescount': page_count,
            'next_page': next_page,
            'pagemenu': True,
            'color_theme': guest.color_theme,
        }
        return HttpResponse(template.render(context, request))
    except:
        return return_error(request)



def show_all_theorems_from_guest(request, guest_id):
    return show_theorems_from_guest(request, guest_id, 'all')


def show_theorems_from_guest(request, guest_id, sort_type):
    return show_theorems_from_guest_page(request, guest_id, sort_type, 1)


def show_theorems_from_guest_page(request, guest_id, sort_type, page_number):
    try:
        guest = open_account_guest(request)
        guest = Guest.objects.get(pk=guest_id)
        theorem_set = guest.theorem_set.all()
        page_count = len(theorem_set)
        next_page = page_number > page_count
        theorems_list = guest.theorem_set.all()[:100]
        template = loader.get_template('math_book/listTheorem.html')
        context = {
            'theorems_list': theorems_list,
            'page_name_text': 'Guest theorems',
            'main_link': '/math_book/guest/' + str(guest_id),
            'pages': page_number,
            'pagescount': page_count,
            'next_page': next_page,
            'pagemenu': True,
            'color_theme': guest.color_theme,
        }
        return HttpResponse(template.render(context, request))
    except:
        return return_error(request)



def show_all_definitions_from_guest(request, guest_id):
    return show_definitions_from_guest(request, guest_id, 'all')


def show_definitions_from_guest(request, guest_id, sort_type):
    return show_definitions_from_guest_page(request, guest_id, sort_type, 1)


def show_definitions_from_guest_page(request, guest_id, sort_type, page_number):
    try:
        guest = open_account_guest(request)
        guest = Guest.objects.get(pk=guest_id)
        definition_set = guest.definition_set.all()
        page_count = len(definition_set)
        next_page = page_number > page_count
        definitions_list = guest.definition_set.all()[:100]
        template = loader.get_template('math_book/listDefinition.html')
        context = {
            'definitions_list': definitions_list,
            'page_name_text': 'Guest definitions',
            'main_link': '/math_book/guest/' + str(guest_id),
            'pages': page_number,
            'pagescount': page_count,
            'next_page': next_page,
            'pagemenu': True,
            'color_theme': guest.color_theme,
        }
        return HttpResponse(template.render(context, request))
    except:
        return return_error(request)


def login(request):
    try:
        guest = open_account_guest(request)
        template = loader.get_template('math_book/login.html')
        context = {
            'guest': guest,
            'page_name_text': 'login',
            'color_theme': guest.color_theme,
        }
        return HttpResponse(template.render(context, request))
    except:
        return HttpResponse('error')


def index(request):
    guest = open_account_guest(request)
    template = loader.get_template("math_book/indexAll.html")
    context = {
        'guest': guest,
        'page_name_text': "math_book",
        'color_theme': guest.color_theme,
    }
    return HttpResponse(template.render(context, request))


def send_subject(request, ):
    if True:
        subject_name = su_cut(request.POST['subject_name'], 50)
        subject_text = su_cut(request.POST['subject_text'], 5000)
        picture_href = su_cut(request.POST['picture_href'], 100)
        subject = Subject(subject_name=subject_name, subject_text=subject_text, picture_href=picture_href)
        subject.save()
        subject_id = subject.id
        return HttpResponse(
            'успешно<br><a href="/math_book/main">main page|главная страница</a><br><a href="/math_book/subject/' + str(
                subject_id) + '">show you new subject|просмотретьт ваш subject</a>')
    else:
        return return_error(request)


def get_subject(request, subject_id):
    try:
        guest = open_account_guest(request)
        subject = Subject.objects.get(id=subject_id)
        template = loader.get_template('math_book/thisSubject.html')
        context = {
            'subject': subject,
            'page_name_text': subject.id,
            'color_theme': guest.color_theme,
        }
        return HttpResponse(template.render(context, request))
    except:
        return return_error(request)


def show_all_subject(request):
    return show_subject(request, 'all')


def show_subject(request, sort_type):
    return show_subject_page(request, sort_type, 1)


def show_subject_page(request, sort_type, page_number):
    try:
        guest = open_account_guest(request)
        page_number = max(1, page_number)
        if sort_type == "main":
            subjects_list = Subject.objects.all()[(page_number - 1) * 50:page_number * 50]
        else:
            sort_type = 'main'
            subjects_list = Subject.objects.all()[(page_number - 1) * 50:page_number * 50]
        page_count = len(Subject.objects.all()) // 50 + 1
        next_page = page_number < page_count
        template = loader.get_template('math_book/listSubject.html')
        context = {
            'subjects_list': subjects_list,
            'page_name_text': sort_type,
            'main_link': '/math_book/subjects/' + sort_type,
            'pages': page_number,
            'pagescount': page_count,
            'next_page': next_page,
            'pagemenu': True,
            'color_theme': guest.color_theme,
        }
        return HttpResponse(template.render(context, request))
    except:
        return return_error(request)


def show_all_tickets_from_subject(request, subject_id):
    return show_tickets_from_subject(request, subject_id, 'all')


def show_tickets_from_subject(request, subject_id, sort_type):
    return show_tickets_from_subject_page(request, subject_id, sort_type, 1)


def show_tickets_from_subject_page(request, subject_id, sort_type, page_number):
    try:
        guest = open_account_guest(request)
        subject = Subject.objects.get(pk=subject_id)
        ticket_set = subject.ticket_set.all()
        page_count = len(ticket_set)
        next_page = page_number > page_count
        tickets_list = subject.ticket_set.all()[:100]
        template = loader.get_template('math_book/listTicket.html')
        context = {
            'tickets_list': tickets_list,
            'page_name_text': 'Subject tickets',
            'main_link': '/math_book/subject/' + str(subject_id),
            'pages': page_number,
            'pagescount': page_count,
            'next_page': next_page,
            'pagemenu': True,
            'color_theme': guest.color_theme,
        }
        return HttpResponse(template.render(context, request))
    except:
        return return_error(request)



def show_all_theorems_from_subject(request, subject_id):
    return show_theorems_from_subject(request, subject_id, 'all')


def show_theorems_from_subject(request, subject_id, sort_type):
    return show_theorems_from_subject_page(request, subject_id, sort_type, 1)


def show_theorems_from_subject_page(request, subject_id, sort_type, page_number):
    try:
        guest = open_account_guest(request)
        subject = Subject.objects.get(pk=subject_id)
        theorem_set = subject.theorem_set.all()
        page_count = len(theorem_set)
        next_page = page_number > page_count
        theorems_list = subject.theorem_set.all()[:100]
        template = loader.get_template('math_book/listTheorem.html')
        context = {
            'theorems_list': theorems_list,
            'page_name_text': 'Subject theorems',
            'main_link': '/math_book/subject/' + str(subject_id),
            'pages': page_number,
            'pagescount': page_count,
            'next_page': next_page,
            'pagemenu': True,
            'color_theme': guest.color_theme,
        }
        return HttpResponse(template.render(context, request))
    except:
        return return_error(request)


def show_all_definitions_from_subject(request, subject_id):
    return show_definitions_from_subject(request, subject_id, 'all')


def show_definitions_from_subject(request, subject_id, sort_type):
    return show_definitions_from_subject_page(request, subject_id, sort_type, 1)


def show_definitions_from_subject_page(request, subject_id, sort_type, page_number):
    try:
        guest = open_account_guest(request)
        subject = Subject.objects.get(pk=subject_id)
        definition_set = subject.definition_set.all()
        page_count = len(definition_set)
        next_page = page_number > page_count
        definitions_list = subject.definition_set.all()[:100]
        template = loader.get_template('math_book/listDefinition.html')
        context = {
            'definitions_list': definitions_list,
            'page_name_text': 'Subject definitions',
            'main_link': '/math_book/subject/' + str(subject_id),
            'pages': page_number,
            'pagescount': page_count,
            'next_page': next_page,
            'pagemenu': True,
            'color_theme': guest.color_theme,
        }
        return HttpResponse(template.render(context, request))
    except:
        return return_error(request)


def create_subject(request):
    try:
        guest = open_account_guest(request)
        template = loader.get_template('math_book/createSubject.html')
        context = {
            'guest': guest,
            'page_name_text': "creating subject",
            'color_theme': guest.color_theme,
        }
        return HttpResponse(template.render(context, request))
    except:
        return HttpResponse('error')


def send_university(request, ):
    try:
        university_shortname = su_cut(request.POST['university_shortname'], 50)
        university_name = su_cut(request.POST['university_name'], 100)
        university_site = su_cut(request.POST['university_site'], 50)
        university_text = su_cut(request.POST['university_text'], 5000)
        picture_href = su_cut(request.POST['picture_href'], 100)
        university = University(university_shortname=university_shortname, university_name=university_name,
                                university_site=university_site, university_text=university_text,
                                picture_href=picture_href)
        university.save()
        university_id = university.id
        return HttpResponse(
            'успешно<br><a href="/math_book/main">main page|главная страница</a><br><a href="/math_book/university/' + str(
                university_id) + '">show you new university|просмотретьт ваш university</a>')
    except:
        return return_error(request)


def get_university(request, university_id):
    try:
        guest = open_account_guest(request)
        university = University.objects.get(id=university_id)
        template = loader.get_template('math_book/thisUniversity.html')
        context = {
            'university': university,
            'page_name_text': university.id,
            'color_theme': guest.color_theme,
        }
        return HttpResponse(template.render(context, request))
    except:
        return return_error(request)


def show_all_university(request):
    return show_university(request, 'all')


def show_university(request, sort_type):
    return show_university_page(request, sort_type, 1)


def show_university_page(request, sort_type, page_number):
    try:
        guest = open_account_guest(request)
        page_number = max(1, page_number)
        if sort_type == "main":
            universitys_list = University.objects.all()[(page_number - 1) * 50:page_number * 50]
        else:
            sort_type = 'main'
            universitys_list = University.objects.all()[(page_number - 1) * 50:page_number * 50]
        page_count = len(University.objects.all()) // 50 + 1
        next_page = page_number < page_count
        template = loader.get_template('math_book/listUniversity.html')
        context = {
            'universitys_list': universitys_list,
            'page_name_text': sort_type,
            'main_link': '/math_book/universitys/' + sort_type,
            'pages': page_number,
            'pagescount': page_count,
            'next_page': next_page,
            'pagemenu': True,
            'color_theme': guest.color_theme,
        }
        return HttpResponse(template.render(context, request))
    except:
        return return_error(request)



def show_all_tickets_from_university(request, university_id):
    return show_tickets_from_university(request, university_id, 'all')


def show_tickets_from_university(request, university_id, sort_type):
    return show_tickets_from_university_page(request, university_id, sort_type, 1)


def show_tickets_from_university_page(request, university_id, sort_type, page_number):
    try:
        guest = open_account_guest(request)
        university = University.objects.get(pk=university_id)
        ticket_set = university.ticket_set.all()
        page_count = len(ticket_set)
        next_page = page_number > page_count
        tickets_list = university.ticket_set.all()[:100]
        template = loader.get_template('math_book/listTicket.html')
        context = {
            'tickets_list': tickets_list,
            'page_name_text': 'University tickets',
            'main_link': '/math_book/university/' + str(university_id),
            'pages': page_number,
            'pagescount': page_count,
            'next_page': next_page,
            'pagemenu': True,
            'color_theme': guest.color_theme,
        }
        return HttpResponse(template.render(context, request))
    except:
        return return_error(request)



def show_all_sessions_from_university(request, university_id):
    return show_sessions_from_university(request, university_id, 'all')


def show_sessions_from_university(request, university_id, sort_type):
    return show_sessions_from_university_page(request, university_id, sort_type, 1)


def show_sessions_from_university_page(request, university_id, sort_type, page_number):
    try:
        guest = open_account_guest(request)
        university = University.objects.get(pk=university_id)
        session_set = university.session_set.all()
        page_count = len(session_set)
        next_page = page_number > page_count
        sessions_list = university.session_set.all()[:100]
        template = loader.get_template('math_book/listSession.html')
        context = {
            'sessions_list': sessions_list,
            'page_name_text': 'University sessions',
            'main_link': '/math_book/university/' + str(university_id),
            'pages': page_number,
            'pagescount': page_count,
            'next_page': next_page,
            'pagemenu': True,
            'color_theme': guest.color_theme,
        }
        return HttpResponse(template.render(context, request))
    except:
        return return_error(request)



def create_university(request):
    try:
        guest = open_account_guest(request)
        template = loader.get_template('math_book/createUniversity.html')
        context = {
            'guest': guest,
            'page_name_text': "creating university",
            'color_theme': guest.color_theme,
        }
        return HttpResponse(template.render(context, request))
    except:
        return HttpResponse('error')


def send_ticket(request):
    if True:
        university_id = su_cut(request.POST['university_id'], 10)
        university = University.objects.get(id=university_id)
        subject_id = su_cut(request.POST['subject_id'], 10)
        subject = Subject.objects.get(id=subject_id)
        guest = open_account_guest(request)
        ticket_name = set_default_if_empty(su_cut(
            request.POST['ticket_name'], 200), "no name")
        ticket_text = ""
        study_direction = su_cut(request.POST['study_direction'], 50)
        picture_href = su_cut(request.POST['picture_href'], 100)
        ticket_type_private = get_bool_value_from_user(request, "ticket_type_private")

        items_count = int(su_cut(str(request.POST['items_count']), 2))
        for item_number in range(items_count):
            item_number_str = str(item_number)
            item_type = su_cut(request.POST['item' + item_number_str], 20)
            if item_type == "definition":
                item_name = str(su_cut(request.POST['name' + item_number_str], 100))
                item_text = str(su_cut(request.POST['text' + item_number_str], 10000))
                item_image = str(su_cut(request.POST['image' + item_number_str], 100))
                try:
                    item_image_file = request.FILES['image_file' + item_number_str]
                    file_size = item_image_file.size
                    if 100 < file_size < 3000000:
                        fs = FileSystemStorage()
                        filename = fs.save(guest.guest_name+"_"+item_image_file.name, item_image_file)
                        uploaded_file_url = fs.url(filename)
                        item_image = uploaded_file_url
                    elif file_size >= 3000000:
                        return HttpResponse('picture size too big<a href="/math/main">main page</a>')
                    elif file_size > 0:
                        return HttpResponse('picture size not enough big<a href="/math/main">main page</a>')
                    else:
                        pass
                except:
                    pass

                #item_name = generate_item_enters(item_name)
                item_text = generate_item_enters(item_text)
                #item_image = generate_item_enters(item_image)

                definition = Definition(definition_name=item_name, by_guest=guest, definition_text=item_text,
                                        pub_date=timezone.now(), subject=subject, picture_href=item_image)
                definition.save()
                definition_id = definition.id
                ticket_text += " /definition_link id='" + str(definition_id) + "'/ (enter)"
            elif item_type == "definition_link":
                item_text = su_cut(request.POST['text' + item_number_str], 10)
                definition_id = int(item_text)
                ticket_text += " /definition_link id='" + str(definition_id) + "'/ (enter)"
            elif item_type == "theorema":
                item_name = su_cut(request.POST['name' + item_number_str], 100)
                item_text = su_cut(request.POST['text' + item_number_str], 10000)
                item_proof = su_cut(request.POST['proof' + item_number_str], 1000)
                item_image = su_cut(request.POST['image' + item_number_str], 100)
                try:
                    item_image_file = request.FILES['image_file' + item_number_str]
                    file_size = item_image_file.size
                    if 100 < file_size < 3000000:
                        fs = FileSystemStorage()
                        filename = fs.save(guest.guest_name+"_"+item_image_file.name, item_image_file)
                        uploaded_file_url = fs.url(filename)
                        item_image = uploaded_file_url
                    elif file_size >= 3000000:
                        return HttpResponse('picture size too big<a href="/math/main">main page</a>')
                    elif file_size > 0:
                        return HttpResponse('picture size not enough big<a href="/math/main">main page</a>')
                    else:
                        pass
                except:
                    pass

                #item_name = generate_item_enters(item_name)
                item_text = generate_item_enters(item_text)
                #item_image = generate_item_enters(item_image)
                item_proof = generate_item_enters(item_proof)
                theorem = Theorem(theorem_name=item_name, by_guest=guest, theorem_text=item_text,
                                  theorem_proof=item_proof,
                                  pub_date=timezone.now(), subject=subject, picture_href=item_image)
                theorem.save()
                theorem_id = theorem.id
                ticket_text += "/theorem_link id='" + str(theorem_id) + "'/"
            elif item_type == "theorem_link":
                item_text = su_cut(request.POST['text' + item_number_str], 10)
                theorem_id = int(item_text)
                ticket_text += "/theorem_link id='" + str(theorem_id) + "'/"
            elif item_type == "text":
                item_text = su_cut(request.POST['text' + item_number_str], 10000)
                ticket_text += "(enter)" + item_text
            elif item_type == "image":
                item_text = su_cut(request.POST['text' + item_number_str], 100)
                ticket_text += "/image_link href='" + str(item_text) + "'/"
        ticket_text = su_cut(ticket_text, 20000)
        if len(guest.ticket_set.filter(ticket_text=ticket_text)) == 0:
            ticket = guest.ticket_set.create(university=university, subject=subject,
                                             ticket_type_private=ticket_type_private, pub_date=timezone.now(),
                                             ticket_name=ticket_name, ticket_text=ticket_text,
                                             study_direction=study_direction, picture_href=picture_href,
                                             )
            ticket_id = ticket.id
            return HttpResponse(
                'успешно<br><a href="/math_book/main">main page|главная страница</a><br><a href="/math_book/ticket/' + str(
                    ticket_id) + '">back to ticket | обратно к ticket</a>')
        else:
            return HttpResponse(
                'ddos attack identified and reflected <a href="/math_book/main">main page|главная страница(go fuck)</a>')
    else:
        return return_error(request)


def get_ticket(request, ticket_id):
    if True:
        guest = open_account_guest(request)
        ticket = Ticket.objects.get(id=ticket_id)
        ticket_text = generate_definitions_and_theorems(ticket.ticket_text)
        ticket_text = generate_images(ticket_text)
        ticket.ticket_text = ticket_text

        template = loader.get_template('math_book/thisTicket.html')
        context = {
            'ticket': ticket,
            'page_name_text': ticket.id,
            'color_theme': guest.color_theme,
        }
        return HttpResponse(template.render(context, request))
    else:
        return return_error(request)


def show_all_ticket(request):
    return show_ticket(request, 'all')


def show_ticket(request, sort_type):
    return show_ticket_page(request, sort_type, 1)


def show_ticket_page(request, sort_type, page_number):
    try:
        guest = open_account_guest(request)
        page_number = max(1, page_number)
        if sort_type == "main":
            tickets_list = Ticket.objects.filter(ticket_type_private=False)[(page_number - 1) * 50:page_number * 50]
        elif sort_type == "new":
            tickets_list = Ticket.objects.filter(ticket_type_private=False).order_by('-pub_date')[
                           (page_number - 1) * 50:page_number * 50]
        elif sort_type == "best":
            tickets_list = Ticket.objects.filter(ticket_type_private=False).order_by('-vote_for_count',
                                                                                     'vote_against_count')[
                           (page_number - 1) * 50:page_number * 50]
        elif sort_type == "my":
            tickets_list = Ticket.objects.filter(ticket_type_private=False).filter(by_guest=guest)[
                           (page_number - 1) * 50:page_number * 50]
        else:
            sort_type = 'main'
            tickets_list = Ticket.objects.all()[(page_number - 1) * 50:page_number * 50]
        page_count = len(Ticket.objects.filter(ticket_type_private=False)) // 50 + 1
        next_page = page_number < page_count
        template = loader.get_template('math_book/listTicket.html')
        context = {
            'tickets_list': tickets_list,
            'page_name_text': sort_type,
            'main_link': '/math_book/tickets/' + sort_type,
            'pages': page_number,
            'pagescount': page_count,
            'next_page': next_page,
            'pagemenu': True,
            'color_theme': guest.color_theme,
        }
        return HttpResponse(template.render(context, request))
    except:
        return return_error(request)


ticket_search_tree = None


def first_search_ticket():
    global ticket_search_tree
    if ticket_search_tree is None:
        ticket_search_tree = NameTree(Ticket, "vote_for_count", "ticket_name")
        ticket_search_tree.create(Ticket.objects.all())

def search_ticket(request):
    # print(set(dir(Guest)) - set(dir(Guest_session)))
    global ticket_search_tree
    first_search_ticket()
    guest = open_account_guest(request)
    sort_type = 'search'

    if request.method == 'POST':
        string_search = request.POST['string_search']
        tickets_list_id = ticket_search_tree.search_with_mistakes(
            string_search, return_only_id=True)
        tickets_list = Ticket.objects.filter(id__in=tickets_list_id)
        last_question = string_search
    else:
        tickets_list = ""
        last_question = ""
    template = loader.get_template('math_book/searchTicket.html')
    context = {
        'last_question': last_question,
        'tickets_list': tickets_list,
        'page_name_text': 'поиск',
        'main_link': '/math_book/tickets/' + sort_type,
        'pagemenu': True,
        'color_theme': guest.color_theme,
    }
    return HttpResponse(template.render(context, request))


def create_ticket(request):
    try:
        guest = open_account_guest(request)
        template = loader.get_template('math_book/createTicket.html')
        context = {
            'guest': guest,
            'page_name_text': 'creating ticket',
            'color_theme': guest.color_theme,
        }
        return HttpResponse(template.render(context, request))
    except:
        return HttpResponse('error')


def send_vote_ticket(request, ticket_id, vote_type):
    if True:
        ticket = Ticket.objects.get(id=ticket_id)
        guest = open_account_guest(request)
        if vote_type == "vote_for":
            vote_type = True
        elif vote_type == "vote_against":
            vote_type = False
        else:
            vote_type = True
            return HttpResponse("нет такого варианта голоса")
        if len(ticket.vote_ticket_set.filter(by_guest=guest)) <= 0:
            if vote_type == True:
                ticket.vote_for_count = ticket.vote_for_count + 1
                ticket.save()
            elif vote_type == False:
                ticket.vote_against_count = ticket.vote_against_count + 1
                ticket.save()
            vote_ticket = Vote_ticket(ticket=ticket, vote_type=vote_type, by_guest=guest)
            vote_ticket.save()
            return get_ticket(request, ticket_id)
        else:
            if ticket.vote_ticket_set.get(by_guest=guest).vote_type == vote_type:
                template = loader.get_template('math_book/thisTicket.html')
                context = {
                    'ticket': ticket,
                    'page_name_text': ticket.id,
                    'color_theme': open_account_guest(request).color_theme,
                    'alert': 'вы уже поставили такую оценку'
                }
                return HttpResponse(template.render(context, request))
            else:
                if vote_type == True:
                    ticket.vote_against_count = ticket.vote_against_count - 1
                    ticket.vote_for_count = ticket.vote_for_count + 1
                    ticket.save()
                elif vote_type == False:
                    ticket.vote_for_count = ticket.vote_for_count - 1
                    ticket.vote_against_count = ticket.vote_against_count + 1
                    ticket.save()
            vote_ticket = ticket.vote_ticket_set.get(by_guest=guest)
            vote_ticket.vote_type = vote_type
            vote_ticket.save()
            template = loader.get_template('math_book/thisTicket.html')
            context = {
                'ticket': ticket,
                'page_name_text': ticket.id,
                'color_theme': open_account_guest(request).color_theme,
            }
            return HttpResponse(template.render(context, request))
    else:
        return return_error(request)


def send_session(request):
    try:
        university_id = su_cut(request.POST['university_id'], 10)
        university = University.objects.get(id=university_id)
        guest = open_account_guest(request)
        session_name = su_cut(request.POST['session_name'], 50)
        session_text = su_cut(request.POST['session_text'], 10000)
        if len(guest.session_set.filter(session_text=session_text)) == 0:
            guest.session_set.create(university=university, session_name=session_name, session_text=session_text)
            session_id = guest.session_set.get(session_name=session_name).id
            return HttpResponse(
                'успешно<br><a href="/math_book/main">main page|главная страница</a><br><a href="/math_book/session/' + str(
                    session_id) + '">back to session | обратно к session</a>')
        else:
            return HttpResponse(
                'ddos attack identified and reflected <a href="/math_book/main">main page|главная страница(go fuck)</a>')
    except:
        return return_error(request)


def get_session(request, session_id):
    if True:
        guest = open_account_guest(request)
        session = Session.objects.get(id=session_id)
        template = loader.get_template('math_book/thisSession.html')
        tickets = session.sorted_tickets()
        context = {
            'is_me': guest==session.by_guest,
            'session': session,
            'page_name_text': session.id,
            'color_theme': guest.color_theme,
            'tickets': tickets
        }
        return HttpResponse(template.render(context, request))
    else:
        return return_error(request)


def remove_ticket_from_session(request, session_id, ticket_id):
    if True:
        guest = open_account_guest(request)
        session = Session.objects.get(id=session_id)
        ticket = session.tickets_with_numbers.get(id=ticket_id)
        if guest == session.by_guest:
            session.tickets_with_numbers.remove(ticket)
        else:
            return_error(request)
        return get_session(request, session_id)
    else:
        return return_error(request)


def add_ticket_to_session(request):
    if True:
        guest = open_account_guest(request)
        session_id = int(su_cut(request.POST['session_id'], 10))
        ticket_id = int(su_cut(request.POST['ticket_id'], 10))
        ticket_number = int(su_cut(request.POST['ticket_number'], 10))
        ticket = Ticket.objects.get(id=ticket_id)
        session = Session.objects.get(id=session_id)
        if guest == session.by_guest:
            session.tickets_with_numbers.add(ticket,
                through_defaults={'ticket_number': ticket_number})
        else:
            return_error(request)
        return get_session(request, session_id)
    else:
        return return_error(request)


def show_all_session(request):
    return show_session(request, 'all')


def show_session(request, sort_type):
    return show_session_page(request, sort_type, 1)


def show_session_page(request, sort_type, page_number):
    try:
        guest = open_account_guest(request)
        page_number = max(1, page_number)
        if sort_type == "main":
            sessions_list = Session.objects.all()[(page_number - 1) * 50:page_number * 50]
        elif sort_type == "my":
            sessions_list = Session.objects.filter(by_guest=guest)[(page_number - 1) * 50:page_number * 50]
        else:
            sort_type = 'main'
            sessions_list = Session.objects.all()[(page_number - 1) * 50:page_number * 50]
        page_count = len(Session.objects.all()) // 50 + 1
        next_page = page_number < page_count
        template = loader.get_template('math_book/listSession.html')
        context = {
            'sessions_list': sessions_list,
            'page_name_text': sort_type,
            'main_link': '/math_book/sessions/' + sort_type,
            'pages': page_number,
            'pagescount': page_count,
            'next_page': next_page,
            'pagemenu': True,
            'color_theme': guest.color_theme,
        }
        return HttpResponse(template.render(context, request))
    except:
        return return_error(request)



def create_session(request):
    try:
        guest = open_account_guest(request)
        template = loader.get_template('math_book/createSession.html')
        context = {
            'guest': guest,
            'page_name_text': 'creating session',
            'color_theme': guest.color_theme,
        }
        return HttpResponse(template.render(context, request))
    except:
        return return_error(request)



def send_theorem(request):
    if True:
        subject_id = su_cut(request.POST['subject_id'], 10)
        subject = Subject.objects.get(id=subject_id)
        guest = open_account_guest(request)
        theorem_name = su_cut(request.POST['theorem_name'], 50)
        theorem_text = su_cut(request.POST['theorem_text'], 10000)
        theorem_proof = su_cut(request.POST['theorem_proof'], 10000)
        picture_href = su_cut(request.POST['picture_href'], 100)
        if len(guest.theorem_set.filter(theorem_text=theorem_text)) == 0:
            guest.theorem_set.create(subject=subject, theorem_name=theorem_name, theorem_text=theorem_text,
                                     theorem_proof=theorem_proof, picture_href=picture_href, pub_date=timezone.now())
            theorem_id = guest.theorem_set.get(theorem_name=theorem_name).id

            information_return = 'успешно<br><a href="/math_book/main">main page|главная страница</a><br><a href="/math_book/theorem/' \
                                 + str(theorem_id) + '">back to theorem | обратно к theorem</a>'
            return return_information(request, information_return)
        else:
            information_return = 'ddos attack identified and reflected <a href="/math_book/main">main page|главная страница(go fuck)</a>'
            return return_information(request, information_return)

    else:
        return return_error(request)



def get_theorem(request, theorem_id):
    try:
        guest = open_account_guest(request)
        theorem = Theorem.objects.get(id=theorem_id)
        template = loader.get_template('math_book/thisTheorem.html')
        context = {
            'theorem': theorem,
            'page_name_text': theorem.id,
            'color_theme': guest.color_theme,
        }
        return HttpResponse(template.render(context, request))
    except Theorem.DoesNotExist:
        return HttpResponse('theorem not found')
    except:
        return return_error(request)



def show_all_theorem(request):
    return show_theorem(request, 'all')


def show_theorem(request, sort_type):
    return show_theorem_page(request, sort_type, 1)


def show_theorem_page(request, sort_type, page_number):
    try:
        guest = open_account_guest(request)
        page_number = max(1, page_number)
        if sort_type == "main":
            theorems_list = Theorem.objects.all()[(page_number - 1) * 50:page_number * 50]
        elif sort_type == "new":
            theorems_list = Theorem.objects.all().order_by('-pub_date')[(page_number - 1) * 50:page_number * 50]
        elif sort_type == "best":
            theorems_list = Theorem.objects.all().order_by('-vote_for_count', 'vote_against_count')[
                            (page_number - 1) * 50:page_number * 50]
        elif sort_type == "my":
            theorems_list = Theorem.objects.filter(by_guest=guest)[(page_number - 1) * 50:page_number * 50]
        else:
            sort_type = 'main'
            theorems_list = Theorem.objects.all()[(page_number - 1) * 50:page_number * 50]
        page_count = len(Theorem.objects.all()) // 50 + 1
        next_page = page_number < page_count
        template = loader.get_template('math_book/listTheorem.html')
        context = {
            'theorems_list': theorems_list,
            'page_name_text': sort_type,
            'main_link': '/math_book/theorems/' + sort_type,
            'pages': page_number,
            'pagescount': page_count,
            'next_page': next_page,
            'pagemenu': True,
            'color_theme': guest.color_theme,
        }
        return HttpResponse(template.render(context, request))
    except:
        return return_error(request)



def create_theorem(request):
    try:
        guest = open_account_guest(request)
        template = loader.get_template('math_book/createTheorem.html')
        context = {
            'guest': guest,
            'color_theme': guest.color_theme,
        }
        return HttpResponse(template.render(context, request))
    except:
        return return_error(request)



def send_vote_theorem(request, theorem_id, vote_type):
    try:
        theorem = Theorem.objects.get(id=theorem_id)
        guest = open_account_guest(request)
        if vote_type == "vote_for":
            vote_type = True
        elif vote_type == "vote_against":
            vote_type = False
        else:
            vote_type = True
            return HttpResponse("нет такого варианта голоса")
        if len(theorem.vote_theorem_set.filter(by_guest=guest)) <= 0:
            if vote_type == True:
                theorem.vote_for_count = theorem.vote_for_count + 1
                theorem.save()
            elif vote_type == False:
                theorem.vote_against_count = theorem.vote_against_count + 1
                theorem.save()
            vote_theorem = Vote_theorem(theorem=theorem, vote_type=vote_type, by_guest=guest)
            vote_theorem.save()
            template = loader.get_template('math_book/thisTheorem.html')
            context = {
                'theorem': theorem,
                'color_theme': open_account_guest(request).color_theme,
            }
            return HttpResponse(template.render(context, request))
        else:
            if theorem.vote_theorem_set.get(by_guest=guest).vote_type == vote_type:
                template = loader.get_template('math_book/thisTheorem.html')
                context = {
                    'theorem': theorem,
                    'color_theme': open_account_guest(request).color_theme,
                    'alert': 'вы уже поставили такую оценку'
                }
                return HttpResponse(template.render(context, request))
            else:
                if vote_type == True:
                    theorem.vote_against_count = theorem.vote_against_count - 1
                    theorem.vote_for_count = theorem.vote_for_count + 1
                    theorem.save()
                elif vote_type == False:
                    theorem.vote_for_count = theorem.vote_for_count - 1
                    theorem.vote_against_count = theorem.vote_against_count + 1
                    theorem.save()
            vote_theorem = theorem.vote_theorem_set.get(by_guest=guest)
            vote_theorem.vote_type = vote_type
            vote_theorem.save()
            template = loader.get_template('math_book/thisTheorem.html')
            context = {
                'theorem': theorem,
                'color_theme': open_account_guest(request).color_theme,
            }
            return HttpResponse(template.render(context, request))
    except:
        return return_error(request)



def send_definition(request):
    try:
        subject_id = su_cut(request.POST['subject_id'], 10)
        subject = Subject.objects.get(id=subject_id)
        guest = open_account_guest(request)
        definition_name = su_cut(request.POST['definition_name'], 50)
        definition_text = su_cut(request.POST['definition_text'], 10000)
        picture_href = su_cut(request.POST['picture_href'], 100)
        if len(guest.definition_set.filter(definition_text=definition_text)) == 0:
            guest.definition_set.create(subject=subject, pub_date=timezone.now(), definition_name=definition_name,
                                        definition_text=definition_text, picture_href=picture_href)
            definition_id = guest.definition_set.get(definition_name=definition_name).id
            return HttpResponse(
                'успешно<br><a href="/math_book/main">main page|главная страница</a><br><a href="/math_book/definition/' + str(
                    definition_id) + '">back to definition | обратно к definition</a>')
        else:
            return HttpResponse(
                'ddos attack identified and reflected <a href="/math_book/main">main page|главная страница(go fuck)</a>')
    except:
        return return_error(request)


def get_definition(request, definition_id):
    try:
        guest = open_account_guest(request)
        definition = Definition.objects.get(id=definition_id)
        template = loader.get_template('math_book/thisDefinition.html')
        context = {
            'definition': definition,
            'page_name_text': definition.id,
            'color_theme': guest.color_theme,
        }
        return HttpResponse(template.render(context, request))
    except:
        return return_error(request)


def show_all_definition(request):
    return show_definition(request, 'all')


def show_definition(request, sort_type):
    return show_definition_page(request, sort_type, 1)


def show_definition_page(request, sort_type, page_number):
    try:
        guest = open_account_guest(request)
        page_number = max(1, page_number)
        if sort_type == "main":
            definitions_list = Definition.objects.all()[(page_number - 1) * 50:page_number * 50]
        elif sort_type == "new":
            definitions_list = Definition.objects.all().order_by('-pub_date')[(page_number - 1) * 50:page_number * 50]
        elif sort_type == "best":
            definitions_list = Definition.objects.all().order_by('-vote_for_count', 'vote_against_count')[
                               (page_number - 1) * 50:page_number * 50]
        elif sort_type == "my":
            definitions_list = Definition.objects.filter(by_guest=guest)[(page_number - 1) * 50:page_number * 50]
        else:
            sort_type = 'main'
            definitions_list = Definition.objects.all()[(page_number - 1) * 50:page_number * 50]
        page_count = len(Definition.objects.all()) // 50 + 1
        next_page = page_number < page_count
        template = loader.get_template('math_book/listDefinition.html')
        context = {
            'definitions_list': definitions_list,
            'page_name_text': sort_type,
            'main_link': '/math_book/definitions/' + sort_type,
            'pages': page_number,
            'pagescount': page_count,
            'next_page': next_page,
            'pagemenu': True,
            'color_theme': guest.color_theme,
        }
        return HttpResponse(template.render(context, request))
    except:
        return return_error(request)


def create_definition(request):
    try:
        guest = open_account_guest(request)
        template = loader.get_template('math_book/createDefinition.html')
        context = {
            'guest': guest,
            'page_name_text': 'creating definition',
            'color_theme': guest.color_theme,
        }
        return HttpResponse(template.render(context, request))
    except:
        return return_error(request)


def send_vote_definition(request, definition_id, vote_type):
    try:
        definition = Definition.objects.get(id=definition_id)
        guest = open_account_guest(request)
        if vote_type == "vote_for":
            vote_type = True
        elif vote_type == "vote_against":
            vote_type = False
        else:
            vote_type = True
            return HttpResponse("нет такого варианта голоса")
        if len(definition.vote_definition_set.filter(by_guest=guest)) <= 0:
            if vote_type == True:
                definition.vote_for_count = definition.vote_for_count + 1
                definition.save()
            elif vote_type == False:
                definition.vote_against_count = definition.vote_against_count + 1
                definition.save()
            vote_definition = Vote_definition(definition=definition, vote_type=vote_type, by_guest=guest)
            vote_definition.save()
            template = loader.get_template('math_book/thisDefinition.html')
            context = {
                'definition': definition,
                'color_theme': open_account_guest(request).color_theme,
            }
            return HttpResponse(template.render(context, request))
        else:
            if definition.vote_definition_set.get(by_guest=guest).vote_type == vote_type:
                template = loader.get_template('math_book/thisDefinition.html')
                context = {
                    'definition': definition,
                    'color_theme': open_account_guest(request).color_theme,
                    'alert': 'вы уже поставили такую оценку'
                }
                return HttpResponse(template.render(context, request))
            else:
                if vote_type == True:
                    definition.vote_against_count = definition.vote_against_count - 1
                    definition.vote_for_count = definition.vote_for_count + 1
                    definition.save()
                elif vote_type == False:
                    definition.vote_for_count = definition.vote_for_count - 1
                    definition.vote_against_count = definition.vote_against_count + 1
                    definition.save()
            vote_definition = definition.vote_definition_set.get(by_guest=guest)
            vote_definition.vote_type = vote_type
            vote_definition.save()
            template = loader.get_template('math_book/thisDefinition.html')
            context = {
                'definition': definition,
                'color_theme': open_account_guest(request).color_theme,
            }
            return HttpResponse(template.render(context, request))
    except:
        return return_error(request)
