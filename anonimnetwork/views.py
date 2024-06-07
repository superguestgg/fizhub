from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect,\
    HttpResponseServerError, HttpResponseBadRequest
from .models import Room, Message
from django.template import loader
from django.urls import reverse
from .room_tree import create, get, tree_create_room
from .rooms_popularity import restart_top_of_rooms, get_top_of_rooms, update_top_of_rooms
import random
import time

from .views_helper import su_cut, generate_random_key, set_default_if_empty, get_bool_value_from_request, Links


def recount_answers(request):
    for message in Message.objects.all():
        answers_count = len(Message.objects.filter(answer_for=message.id))
        if message.answers_count == answers_count:
            continue
        message.answers_count = answers_count
        message.save()
    return HttpResponse("successful")


# не используется
def start2():
    for message in Message.objects.all():
        message.answers_count = len(Message.objects.filter(answer_for=message.id))
        message.save()


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
        create()
        restart_top_of_rooms()
    requests_count += 1


def anti_ddos_decorator(func):
    def new_func(request, *args, **kwargs):
        calculate_request()
        if anti_ddos(request):
            return func(request, *args, **kwargs)
        else:
            return HttpResponseServerError()
            #return HttpResponse("sorry, it seems it a ddos attack")

    new_func.__doc__ = func.__doc__
    new_func.__name__ = func.__name__
    return new_func


@anti_ddos_decorator
def list_rooms(request, sort_type, page_number=1):
    page_number = int(page_number)
    page_number = max(1, page_number)
    #print(sort_type, page_number)
    if sort_type == "main":
        page_count = (len(Room.objects.filter(room_type_private=False))) // 50 + 1
        public_rooms_list = Room.objects.filter(room_type_private=False)[(page_number - 1) * 50:(page_number) * 50]
    elif sort_type in ["new", "newrooms"]:
        page_count = len(Room.objects.filter(room_type_private=False)) // 50 + 1
        public_rooms_list = (Room.objects.filter(room_type_private=False)[::-1])[
                           (page_number - 1) * 50:(page_number) * 50]
    elif sort_type in ["top", "toprooms"]:
        top = get_top_of_rooms()
        # top[0].sort() это не нужно, тк сортировка теряется при запросе к бд "id__id"
        page_count = len(top[0]) // 50 + 1
        public_rooms_list = Room.objects.filter(id__in=top[0])[(page_number - 1) * 50:(page_number) * 50]
    elif sort_type == "channels":
        page_count = len(Room.objects.filter(room_type_private=False, room_type_channel=True)) // 50 + 1
        public_rooms_list = (Room.objects.filter(room_type_channel=True, room_type_private=False)[::-1])[
                           (page_number - 1) * 50:page_number * 50]
    else:
        print(sort_type, page_number)
        return HttpResponse("what")

    next_page = (page_count > page_number)
    template = loader.get_template('anonimnetwork/listRoom.html')
    context = {
        'publicrooms_list': public_rooms_list,
        'pages': page_number,
        'pagescount': page_count,
        'page_name': sort_type,
        'next_page': next_page
    }
    return HttpResponse((template.render(context, request)))


def main(request):
    return list_rooms(request, "main")


def open_room_from_request(request, room_name):
    try:
        this_room = Room.objects.get(room_name=room_name)
    except Room.DoesNotExist:
        return False, HttpResponse("Room does not exist")

    if not this_room.room_type_password:
        return True, this_room
    if 'roompassword' in request.POST:
        room_password = request.POST['roompassword'][:50]
        if this_room.room_password == room_password:
            return True, this_room
        elif len(room_password) != 0:
            return False, HttpResponse('password incorrect, whatsapp suck')
    if 'password' in request.COOKIES:
        room_password = request.COOKIES['password'][:50]
        if this_room.room_password == room_password:
            return True, this_room
        else:
            return False, render(request, 'anonimnetwork/roompass.html', {'room': this_room})
    else:
        return False, render(request, 'anonimnetwork/roompass.html', {'room': this_room})


def can_change_room(request, room_name):
    can_see, this_room = open_room_from_request(request, room_name)
    if not can_see:
        return can_see, this_room

    if not this_room.room_type_channel:
        return True, this_room
    if 'passwordadmin' in request.POST:
        admin_password = request.POST['passwordadmin'][:50]
        if this_room.room_channel_admin_password == admin_password:
            return True, this_room
    if 'passwordadmin' in request.COOKIES:
        admin_password = request.COOKIES['passwordadmin'][:50]
        if this_room.room_channel_admin_password == admin_password:
            return True, this_room
    else:
        return False, HttpResponse(f"admin password incorrect<br>{Links.main_page}")




@anti_ddos_decorator
def theme(request):
    if request.method == 'POST':
        theme_name = request.POST['theme']
        publicrooms_list = Room.objects.filter(room_theme=theme_name, room_type_private=False)
        page_count = len(publicrooms_list) // 50 + 1
        page_number = 1
        next_page = page_count > page_number
        template = loader.get_template('anonimnetwork/listRoom.html')
        context = {
            'publicrooms_list': publicrooms_list,
            'pages': page_number,
            'pagescount': page_count,
            'page_name': 'theme',
            'next_page': next_page
        }
        return HttpResponse(template.render(context, request))
    else:
        return render(request, 'anonimnetwork/theme.html')


@anti_ddos_decorator
def theme_page(request, page_number):
    if anti_ddos(request):
        try:
            calculate_request()
            theme_name = request.POST['theme']
            publicrooms_list = Room.objects.filter(room_theme=theme_name, room_type_private=False)[
                               (page_number - 1) * 50:(page_number) * 50]
            page_count = len(publicrooms_list) // 50 + 1
            page_number = page_number
            next_page = page_count > page_number
            template = loader.get_template('anonimnetwork/listRoom.html')
            context = {
                'publicrooms_list': publicrooms_list,
                'pages': page_number,
                'pagescount': page_count,
                'page_name': 'theme',
                'next_page': next_page
            }
            return HttpResponse(template.render(context, request))
        except:
            return render(request, 'anonimnetwork/theme.html')
    else:
        return HttpResponse("sorry, it seems it a ddos attack")


def themeget(request, theme_name):
    return themeget_page(request, theme_name, 1)


@anti_ddos_decorator
def themeget_page(request, theme_name, page_number):
    try:
        publicrooms_list = Room.objects.filter(room_theme=theme_name, room_type_private=False)[
                           (page_number - 1) * 50:(page_number) * 50]
        template = loader.get_template('anonimnetwork/listRoom.html')
        page_count = len(publicrooms_list) // 50 + 1

        next_page = page_count > page_number
        context = {
            'publicrooms_list': publicrooms_list,
            'pages': page_number,
            'pagescount': page_count,
            'page_name': 'theme',
            'next_page': next_page
        }
        return HttpResponse(template.render(context, request))
    except:
        return render(request, 'anonimnetwork/theme.html')


@anti_ddos_decorator
def create_room(request):
    try:
        template = loader.get_template('anonimnetwork/createroom.html')
        context = {

        }
        return HttpResponse(template.render(context, request))
    except:
        return HttpResponse(f"server error <br>{Links.main_page}")


@anti_ddos_decorator
def spam_room(request, room_count):
    for i in range(room_count):
        room_name = generate_random_key(key_length=random.randint(5, 50))
        new_room = Room(room_name=room_name)
        new_room.save()
    return HttpResponse(request, "hack succesful")


@anti_ddos_decorator
def send_room(request):
    room_name = request.POST['room_name'].replace("/", "").replace('\\', "")[:100]
    room_theme = request.POST['room_theme'].replace("/", "").replace('\\', "")[:50]
    room_description = request.POST['room_description'][:1000]
    room_password = request.POST['room_password'][:50]
    room_channel_admin_password = request.POST['room_channel_admin_password'][:50]
    room_type_private = get_bool_value_from_request(request, 'room_type_private')
    room_type_channel = get_bool_value_from_request(request, 'room_type_channel')
    room_type_password = get_bool_value_from_request(request, 'room_type_password')
    room_type_token = get_bool_value_from_request(request, 'room_type_token')

    if len(Room.objects.filter(room_name=room_name)) > 0:
        return HttpResponse(f"name reserved <br>{Links.main_page}")
    if len(room_name) == 0:
        return HttpResponse(f"you can't create a room without name <br>{Links.main_page}")
    room_theme = set_default_if_empty(room_theme, "no theme")
    new_room = Room(room_name=room_name, room_theme=room_theme, room_type_private=room_type_private,
                    room_type_password=room_type_password, room_password=room_password,
                    room_type_token=room_type_token, room_description=room_description,
                    room_type_channel=room_type_channel,
                    room_channel_admin_password=room_channel_admin_password)
    new_room.save()
    try:
        ret = tree_create_room(Room.objects.get(room_name=room_name).id)
        if ret == "e":
            return HttpResponse(
                "succesful created, but error: room hadn't been append to room's tree<br><a href='/anonnetwork/" + str(
                    new_room.room_name) + "'>your room</a>")

    except:
        return HttpResponse(
            "succesful created, but error: room hadn't been append to room's tree<br><a href='/anonnetwork/" + str(
                new_room.room_name) + "'>your room</a>")
    return HttpResponseRedirect(f"/anonnetwork/{new_room.room_name}")


@anti_ddos_decorator
def find_room(request):
    #return HttpResponse(
    #        "server error <br><a href='/anonnetw
    #        ork/main'>main page</a><br><a href='
    #        /anonnetwork/admin'>bug report</a>")

    try:
        string = request.POST['room_name']
        rooms = get(string)
        roomsid = []
        for room in rooms:
            if str(room[0]).isdigit():
                roomsid.append(room[0])
        publicrooms_list = Room.objects.filter(id__in=roomsid)

        template = loader.get_template('anonimnetwork/findroom.html')
        context = {
            'publicrooms_list': publicrooms_list,
            'string': string
        }
        return HttpResponse(template.render(context, request))
    except:
        try:
            return render(request, 'anonimnetwork/findroom.html')
        except:
            return HttpResponse(
                f"server error <br>{Links.main_page}{Links.bug_report}")


@anti_ddos_decorator
def get_room(request):
    try:
        room_name = request.POST['room_name']
        rooms = Room.objects.filter(room_name=room_name)
        if len(rooms) > 0:
            return HttpResponse(Links.room(room_name))
    except:
        return HttpResponse(Links.main_page)


@anti_ddos_decorator
def room(request, room_name):
    can_see, this_room = open_room_from_request(request, room_name)
    if not can_see:
        return this_room
    messages = Message.objects.filter(room_id=this_room.id)
    pinned_messages = messages.filter(is_pinned=True)
    page_count = (len(messages) + 99) // 100
    if len(pinned_messages) > 1:
        pinned_message = pinned_messages[len(pinned_messages) - 1]
    elif len(pinned_messages) == 1:
        pinned_message = pinned_messages[0]
    else:
        pinned_message = False

    message_list = this_room.message_set.order_by('-pub_date')[:100]
    return render(request, 'anonimnetwork/thisRoom.html',
                  {'message_list': message_list,
                   'room': this_room,
                   'pages': 1,
                   'pagescount': page_count,
                   'pinned_message': pinned_message
                   })


def room_threads(request, room_name):
    can_see, this_room = open_room_from_request(request, room_name)
    if not can_see:
        return this_room
    messages = Message.objects.filter(room_id=this_room.id)
    threads_messages = messages.filter(answer_for=0)
    pinned_messages = messages.filter(is_pinned=True)
    page_count = (len(threads_messages) + 99) // 100
    if len(pinned_messages) >= 1:
        pinned_message = pinned_messages[len(pinned_messages) - 1]
    else:
        pinned_message = False

    message_list = threads_messages.order_by('-pub_date')[:100]

    return render(request, 'anonimnetwork/thisRoom.html',
                  {'message_list': message_list,
                   'room': this_room,
                   'pages': 1,
                   'pagescount': page_count,
                   'pinned_message': pinned_message
                   })


@anti_ddos_decorator
def room_admin(request, room_name):
    can_see, this_room = open_room_from_request(request, room_name)
    if not can_see:
        return this_room
    this_room = Room.objects.get(room_name=room_name)
    messages = Message.objects.filter(room_id=this_room.id)
    page_count = (len(messages) + 99) // 100

    message_list = this_room.message_set.order_by('-pub_date')[:100]
    return render(request, 'anonimnetwork/thisRoom.html',
                  {'message_list': message_list, 'room': this_room, 'pages': 1, 'pagescount': page_count,
                   'isadmin': True})


@anti_ddos_decorator
def room_pass(request, room_name):
    return HttpResponse(f"это устаревшая ссылка, она уже не поддерживается<br>{Links.room(room_name)}")


@anti_ddos_decorator
def room_page(request, room_name, page_number):
    can_see, this_room = open_room_from_request(request, room_name)
    if not can_see:
        return this_room
    page_number = max(page_number, 1)
    messages = Message.objects.filter(room_id=this_room.id)
    page_count = (len(messages) + 99) // 100
    message_list = this_room.message_set.order_by('-pub_date')[(page_number - 1) * 100:page_number * 100]
    return render(request, 'anonimnetwork/thisRoom.html',
                  {'message_list': message_list, 'room': this_room, 'pages': page_number,
                   'pagescount': page_count})


@anti_ddos_decorator
def pinned_messages(request, room_name):
    can_see, curr_room = open_room_from_request(request, room_name)
    if not can_see:
        return curr_room
    messages = Message.objects.filter(room_id=curr_room.id, is_pinned=True)
    page_count = (len(messages) + 99) // 100
    # pinned_message = {"room_id": curr_room.id, 'answer_for': 0, 'message_text': 'pinned messages'}
    pinned_message = False

    message_list = messages.order_by('-pub_date')[:100]
    return render(request, 'anonimnetwork/thisRoom.html',
                  {'message_list': message_list,
                   'room': curr_room,
                   'pages': 1,
                   'pagescount': page_count,
                   'pinned_message': pinned_message,
                   'is_pined_page': True
                   })


@anti_ddos_decorator
def room_description(request, room_name):
    can_see, this_room = open_room_from_request(request, room_name)
    if not can_see:
        return this_room

    information = this_room.room_description
    context = {
        'information': information,
        'room': this_room
    }
    return render(request, 'anonimnetwork/information.html', context)


@anti_ddos_decorator
def message(request, room_name, message_id):
    can_see, this_room = open_room_from_request(request, room_name)
    if not can_see:
        return this_room

    room_id = this_room.id

    try:
        answer_for = Message.objects.get(id=Message.objects.get(id=message_id, room_id=room_id).answer_for)
    except:
        answer_for = "server error"

    # кажется это не используется
    message_list = Message.objects.filter(id=message_id, room_id=room_id)
    try:
        message = Message.objects.get(id=message_id, room_id=room_id)
    except:
        message = "not found"
    answers_list = Message.objects.filter(answer_for=message_id, room_id=room_id)
    template = loader.get_template('anonimnetwork/thisMessage.html')
    context = {
        'answer_for': answer_for,
        'this_message': message,
        'message_list': message_list,
        'room': this_room,
        'answers_list': answers_list
    }

    return HttpResponse(template.render(context, request))


@anti_ddos_decorator
def message_admin(request, room_name, message_id):
    can_see, this_room = open_room_from_request(request, room_name)
    if not can_see:
        return this_room
    room_id = this_room.id

    try:
        answer_for = Message.objects.get(id=Message.objects.get(id=message_id, room_id=room_id).answer_for)
    except:
        answer_for = "server error"
    message_list = Message.objects.filter(id=message_id, room_id=room_id)
    answers_list = Message.objects.filter(answer_for=message_id, room_id=room_id)
    template = loader.get_template('anonimnetwork/thisMessage.html')
    context = {
        'answer_for': answer_for,
        'message_list': message_list,
        'room': this_room,
        'answers_list': answers_list,
        'isadmin': True
    }

    return HttpResponse(template.render(context, request))


@anti_ddos_decorator
def send_message(request, room_name):
    can_send, this_room = can_change_room(request, room_name)
    if not can_send:
        return this_room

    message_text = request.POST['textarea'][:2000]
    if len(message_text) <= 0:
        return HttpResponse(f"недостаточная длина сообщения<br>{Links.main_page}{Links.room(room_name)}")

    if this_room.room_rights >= 0:
        this_room.message_set.create(message_text=message_text, pub_date=timezone.now())
        this_room.room_messages_count = this_room.room_messages_count + 1
        this_room.save()
        if not this_room.room_type_private:
            update_top_of_rooms(this_room.id)
        return HttpResponseRedirect(f'/anonnetwork/{room_name}/')
    """elif user.guest_rights>=1:
        try:
            userfile = request.FILES['file']
            filesize= userfile.size
            if filesize>100 and filesize<3000000:
                fs = FileSystemStorage()
                filename = fs.save(creator_name+"_"+userfile.name, userfile)
                uploaded_file_url = fs.url(filename)
                user.task_set.create(task_name=task_name, task_text=task_text, pub_date=timezone.now(),picture_href=uploaded_file_url, theme1_name=theme1_name, theme2_name=theme2_name)
                user.guest_rights=user.guest_rights-1
                user.save()
                return HttpResponse('succesful <br> <a href="/physic-in-sesc/main">main page</a>')
            elif  filesize>=3000000:
                return HttpResponse('picture size too big<a href="/physic-in-sesc/main">main page</a>')
            elif filesize>0:
                return HttpResponse('picture size not enough big<a href="/physic-in-sesc/main">main page</a>')
            else:
                user.task_set.create(task_name=task_name, task_text=task_text, pub_date=timezone.now(), picture_href=picture_url, theme1_name=theme1_name, theme2_name=theme2_name)
                return HttpResponse('succesful <br> <a href="/physic-in-sesc/main">main page</a>')
        except:
            user.task_set.create(task_name=task_name, task_text=task_text, pub_date=timezone.now(), picture_href=picture_url, theme1_name=theme1_name, theme2_name=theme2_name)
            return HttpResponse('succesful <br> <a href="/physic-in-sesc/main">main page</a>')
    """


@anti_ddos_decorator
def pin_message(request, room_name, message_id):
    return change_message_pinned(request, room_name, message_id, True)


@anti_ddos_decorator
def unpin_message(request, room_name, message_id):
    return change_message_pinned(request, room_name, message_id, False)


def change_message_pinned(request, room_name, message_id, set_status):
    can_change, this_room = can_change_room(request, room_name)
    if not can_change:
        return this_room

    if this_room.room_rights < 0:
        return HttpResponse(f"room banned<br>{Links.main_page}")

    this_message = this_room.message_set.get(id=message_id)
    this_message.is_pinned = set_status
    this_message.save()

    return HttpResponseRedirect(f'/anonnetwork/{room_name}/{message_id}/')


@anti_ddos_decorator
def answer(request, room_name, message_id):
    can_send, this_room = can_change_room(request, room_name)
    if not can_send:
        return this_room

    message_text = request.POST['textarea'][:2000]
    if len(message_text) <= 0:
        return HttpResponse(f"недостаточная длина сообщения<br>{Links.main_page}{Links.room(room_name)}")

    if this_room.room_rights < 0:
        return HttpResponse(f"room banned<br>{Links.main_page}")

    this_room.message_set.create(message_text=message_text, pub_date=timezone.now(), answer_for=message_id)

    this_room.room_messages_count = this_room.room_messages_count + 1
    this_room.save()
    message = Message.objects.get(id=message_id)
    message.answers_count = message.answers_count + 1
    message.save()
    if not this_room.room_type_private:
        update_top_of_rooms(this_room.id)
    return HttpResponseRedirect(f'/anonnetwork/{room_name}/{message_id}/')


"""def useful(request):
    useful_files = Usefulfiles.objects.all()[:50]
    template=loader.get_template('physicsesc/useful.html')
    context = {
        'useful_files': useful_files,
    }
    return HttpResponse(template.render(context,request))
def sendusefulfile(request):
    try:
        filename = request.POST['filename']
        username = request.POST['username']
        userpassword = request.POST['userpassword']
        filehref = request.POST['filehref']
        user=(Guest.objects.get(guest_name=username))
        if user.guest_password==userpassword and filename!="" and filehref!="":
            file=user.usefulfiles_set.create(file_name=filename,file_href=filehref)
            file.save()

            return HttpResponse('succesful')
        else:
            return HttpResponse('not succesful')
    except:
        return HttpResponse('server error<br><a href="/physic-in-sesc/main">main page</a>')
"""
