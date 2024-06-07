from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from .models import Room, Message
from django.template import loader
from django.urls import reverse

branch = []


# самое главное что можно сказать про этот модуль
# - работает и ладно
# (хотя у меня уже есть универсальная замена,
# занимающая меньше строк, более понятная и более стабильная
# (здесь: https://github.com/superguestgg/fizhub/blob/main/math_book/search_tree.py) ,
# но пусть останется для истории
# просто эта штука работает лучше на некоторых запросах
def create():
    global branch
    try:
        print("creating a tree....")
    except:
        branch_length = 1
    branch = [["", "", [], [], [], []]]
    # last letter, all letters, massive of next letters,massive of links for next letters,
    # this room, top room
    branch_length = 1
    rooms = Room.objects.filter(room_type_private=False)

    for room in rooms:
        room_name = (room.room_name)
        room_name_length = len(room_name)
        room_name_list = list(room_name)
        room_messages_count = int(room.room_messages_count)
        place = 0
        for letter in room_name_list:

            if room_name_length == len(branch[place][1]):
                # print(room_name)
                branch[place][4] = [room.id, room.room_name, room.room_messages_count]
            else:
                if branch[place][5] == []:
                    branch[place][5] = [room.id, room.room_name, room.room_messages_count]
                elif branch[place][5][2] < room_messages_count:
                    branch[place][5] = [room.id, room.room_name, room.room_messages_count]

            if branch[place][2].count(letter) == 0:

                branch[place][2].append(letter)
                branch[place][3].append(branch_length)
                if room_name_length == len(str(branch[place][1]) + str(letter)):
                    branch.append([letter, str(branch[place][1]) + str(letter), [], [],
                                   [room.id, room.room_name, room.room_messages_count], []])
                else:
                    branch.append([letter, str(branch[place][1]) + str(letter), [], [], [],
                                   [room.id, room.room_name, room.room_messages_count]])

                place = branch_length
                branch_length += 1

            else:
                place = branch[place][3][branch[place][2].index(letter)]
                if room_name == str(branch[place][1]):
                    # print(room_name)
                    branch[place][4] = [room.id, room.room_name, room.room_messages_count]

    # print(branch)

    file = open("tree.txt", "w")
    for i in range(len(branch)):
        file.write(str(branch[i]))
    print("tree created succesful")


def tree_create_room(room_id):
    global branch

    # last letter, all letters, massive of next letters,massive of links for next letters,
    # this room, top room
    branch_length = len(branch)
    try:
        room = Room.objects.get(id=room_id)

        room_name = (room.room_name)
        room_name_length = len(room_name)
        room_name_list = list(room_name)
        room_messages_count = int(room.room_messages_count)
        place = 0
        for letter in room_name_list:
            if room_name_length == len(branch[place][1]):
                branch[place][4] = [room.id, room.room_name, room.room_messages_count]
            else:
                if branch[place][5] == []:
                    branch[place][5] = [room.id, room.room_name, room.room_messages_count]
                elif branch[place][5][2] < room_messages_count:
                    branch[place][5] = [room.id, room.room_name, room.room_messages_count]

            if branch[place][2].count(letter) == 0:

                branch[place][2].append(letter)
                branch[place][3].append(branch_length)
                if room_name_length == len(str(branch[place][1]) + str(letter)):
                    branch.append([letter, str(branch[place][1]) + str(letter), [], [],
                                   [room.id, room.room_name, room.room_messages_count], []])
                else:
                    branch.append([letter, str(branch[place][1]) + str(letter), [], [], [],
                                   [room.id, room.room_name, room.room_messages_count]])

                place = branch_length
                branch_length += 1

            else:
                place = branch[place][3][branch[place][2].index(letter)]
                if room_name == str(branch[place][1]):
                    print(room_name)
                    branch[place][4] = [room.id, room.room_name, room.room_messages_count]

        return "s"
    except:
        return "e"
    # print(branch)
    # file=open("tree.txt","w")
    # for i in range (len(branch)):
    #    file.write(str(branch[i]))


def searchwitherrors_recursion(string, string_list, place, mistake, indexnow):
    if mistake >= 0:
        if branch[place][0].count("u") > 0:
            print(string, string_list, place, mistake, indexnow)
            print(branch[place])
        let = indexnow
        # letter = string_list[let]
        # print(letter)
        rooms_list = []
        if let < len(string_list):
            letter = string_list[let]
            if letter in branch[place][2]:
                # print(letter)
                for i in range(len(branch[place][3])):
                    if branch[place][2][i] != letter:
                        place2 = branch[place][3][i]
                        rooms_list_append = (
                            searchwitherrors_recursion(string, string_list, place2, mistake - 1, indexnow + 1))
                        if rooms_list_append != None and rooms_list_append != []:
                            # print(rooms_list_append)
                            rooms_list += (rooms_list_append)
                i = branch[place][2].index(letter)
                place2 = branch[place][3][i]
                rooms_list_append = (searchwitherrors_recursion(string, string_list, place2, mistake, indexnow + 1))
                if rooms_list_append != None and rooms_list_append != []:
                    # print(rooms_list_append)
                    rooms_list += (rooms_list_append)
            else:
                for i in range(len(branch[place][3])):
                    place2 = branch[place][3][i]
                    rooms_list_append = (
                        searchwitherrors_recursion(string, string_list, place2, mistake - 1, indexnow + 1))
                    if rooms_list_append != None and rooms_list_append != []:
                        # print(rooms_list_append)
                        rooms_list += (rooms_list_append)
        else:
            print("efve", mistake)
            place2 = place
            if branch[place2][4]:
                rooms_list.append(branch[place2][4])
            for i in range(len(branch[place2][3])):
                # print(branch[place][3][i])
                if branch[int(branch[place2][3][i])][5]:
                    rooms_list.append(branch[branch[place2][3][i]][5])
                if branch[branch[place2][3][i]][4]:
                    rooms_list.append(branch[int(branch[place2][3][i])][4])
            """
            print(branch[place],mistake)
            if letter in branch[place][2]:
                place2 = branch[place][3][branch[place][2].index(letter)]
                if branch[place2][4]:
                    rooms_list.append(branch[place2][4])
                for i in range(len(branch[place2][3])):
                    # print(branch[place][3][i])
                    if branch[int(branch[place2][3][i])][5]:
                        rooms_list.append(branch[branch[place2][3][i]][5])
                    if branch[branch[place2][3][i]][4]:
                        rooms_list.append(branch[int(branch[place2][3][i])][4])
            if mistake > 0:
                print(mistake*100000)
                for letter in branch[place][2]:
                    place2 = branch[place][3][branch[place][2].index(letter)]
                    if branch[place2][4]:
                        rooms_list.append(branch[place2][4])
                    for i in range(len(branch[place2][3])):
                        # print(branch[place][3][i])
                        if branch[int(branch[place2][3][i])][5]:
                            rooms_list.append(branch[branch[place2][3][i]][5])
                        if branch[branch[place2][3][i]][4]:
                            rooms_list.append(branch[int(branch[place2][3][i])][4])
                #break"""
        return rooms_list


def searchwitherrors2(string):
    print("search with errors 2")
    global branch
    branch_length = len(branch)
    room = string
    string_list = list(string)
    string_length = len(string)
    print(string_length)
    # print(string_length)
    rooms_list = []
    mistake = 0
    while len(rooms_list) == 0 and mistake < 10:
        mistake += 1
        print(str(mistake) + "...........")
        place = 0

        rooms_list = searchwitherrors_recursion(string, string_list, place, mistake, 0)

    print(rooms_list)

    return rooms_list


def searchwitherrors(string):
    # print(1)
    global branch
    branch_length = len(branch)
    room = string
    string_list = list(string)
    string_length = len(string)
    print(string_length)
    # print(string_length)
    place = 0
    t = 1
    rooms_list = []
    for let in range(string_length):
        # print(branch[place][1])
        letter = string_list[let]
        # print(letter)
        if letter in branch[place][2]:
            # print(letter)
            for i in range(len(branch[place][3])):
                if branch[place][2][i] != letter:
                    t2 = 1
                    place2 = branch[place][3][i]
                    for let2 in range(let + 1, len(string_list)):
                        letter2 = string_list[let2]
                        if letter2 in branch[place2][2]:
                            place2 = branch[place2][3][branch[place2][2].index(letter2)]
                        else:
                            t2 = 0
                            break
                    if t2 == 1:
                        if branch[place2][4]:
                            rooms_list.append(branch[place2][4])
                        for i in range(len(branch[place2][3])):
                            # print(branch[place][3][i])
                            if branch[int(branch[place2][3][i])][5]:
                                rooms_list.append(branch[branch[place2][3][i]][5])
                            if branch[branch[place2][3][i]][4]:
                                rooms_list.append(branch[int(branch[place2][3][i])][4])
            place = branch[place][3][branch[place][2].index(letter)]
        else:
            # print(999)
            t = 0
            for i in range(len(branch[place][3])):
                # print(branch[place][2][i])
                t2 = 1
                place2 = branch[place][3][i]
                for let2 in range(let + 1, len(string_list)):
                    # print(22)
                    letter2 = string_list[let2]
                    if letter2 in branch[place2][2]:
                        place2 = branch[place2][3][branch[place2][2].index(letter2)]
                    else:
                        t2 = 0
                        break
                if t2 == 1:
                    if branch[place2][4]:
                        rooms_list.append(branch[place2][4])
                    for i in range(len(branch[place2][3])):
                        # print(branch[place][3][i])
                        if branch[int(branch[place2][3][i])][5]:
                            rooms_list.append(branch[branch[place2][3][i]][5])
                        if branch[branch[place2][3][i]][4]:
                            rooms_list.append(branch[int(branch[place2][3][i])][4])
            break

    if t == 1:
        if branch[place][4]:
            rooms_list.append(branch[place][4])
        for i in range(len(branch[place][3])):
            # print(branch[place][3][i])
            if branch[int(branch[place][3][i])][5]:
                rooms_list.append(branch[branch[place][3][i]][5])
            if branch[branch[place][3][i]][4]:
                rooms_list.append(branch[int(branch[place][3][i])][4])
    """if len(rooms_list)==0 or t==0:
        if branch[place][4]:
            rooms_list.append(branch[place][4])
        for i in range (len(branch[place][3])):
            #print(branch[place][3][i])
            if branch[int(branch[place][3][i])][5]:
                rooms_list.append(branch[branch[place][3][i]][5])
            if branch[branch[place][3][i]][4]:
                rooms_list.append(branch[int(branch[place][3][i])][4])"""
    if len(rooms_list) == 0:
        return searchwitherrors2(string)
    return rooms_list


def get(string):
    # print(1)
    global branch
    branch_length = len(branch)
    room = string
    string_list = list(string)
    string_length = len(string)
    # print(string_length)
    place = 0
    t = 1
    for letter in string_list:
        # print(branch[place][1])

        if letter in branch[place][2]:
            place = branch[place][3][branch[place][2].index(letter)]
        else:
            t = 0
            break
    rooms_list = []
    if t == 1:
        if branch[place][4]:
            rooms_list.append(branch[place][4])
        for i in range(len(branch[place][3])):
            # print(branch[place][3][i])
            if branch[int(branch[place][3][i])][5]:
                rooms_list.append(branch[branch[place][3][i]][5])
            if branch[branch[place][3][i]][4]:
                rooms_list.append(branch[int(branch[place][3][i])][4])
    if len(rooms_list) == 0 or t == 0:
        print("search with errors")
        return searchwitherrors(string)
    return rooms_list
