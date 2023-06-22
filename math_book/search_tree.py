from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse


class NameTree:
    def __init__(self, class_search, sort_argument_name, name_argument_name):
        # filter_arg, func_filter_arg_should):
        self.class_search = class_search
        self.sort_argument_name = sort_argument_name
        self.name_argument_name = name_argument_name
        # self.filter_arg = filter_arg
        # self.func_filter_arg_should = func_filter_arg_should
        self.branch = [NameTreeNode("")]

    def create(self, new_objects):
        print("creating a tree....")
        for new_object in new_objects:
            self.add(new_object)

    def add(self, new_object):
        branch = self.branch
        obj_name = getattr(new_object, self.name_argument_name)
        obj_name_list = list(obj_name)
        obj_sort_argument = int(getattr(new_object, self.sort_argument_name))
        obj = [new_object.id, obj_sort_argument]
        place = 0
        for letter in obj_name_list:
            if branch[place].top_child_obj is None:
                branch[place].top_child_obj = obj
            elif branch[place].top_child_obj[1] < obj_sort_argument:
                branch[place].top_child_obj = obj

            if letter not in branch[place].next_letters:
                branch[place].next_letters[letter] = len(branch)
                branch.append(NameTreeNode(branch[place].all_path + letter))
            place = branch[place].next_letters[letter]
        if branch[place].curr_obj is None:
            branch[place].curr_obj = obj
        elif branch[place].curr_obj[1] < obj_sort_argument:
            branch[place].curr_obj = obj
        return

    def search(self, string_search):
        branch = self.branch
        place = 0
        obj_list = []
        for letter in string_search:
            if letter in branch[place].next_letters:
                place = branch[place].next_letters[letter]
        if not branch[place].curr_obj is None:
            obj_list.append(branch[place].curr_obj)
        if not branch[place].top_child_obj is None:
            obj_list.append(branch[place].top_child_obj)
        for key_val_pair in branch[place].next_letters.items():
            child = branch[key_val_pair[1]]
            if not child.top_child_obj is None:
                obj_list.append(child.top_child_obj)
            if not child.curr_obj is None:
                obj_list.append(child.curr_obj)
        return obj_list

    def search_with_mistakes(self, string_search, return_only_id=False):
        obj_list = []
        self.search_recursion(string_search, len(string_search) // 2,
                              0, string_search, 0, obj_list)
        if return_only_id:
            return [obj[0] for obj in obj_list]
        return obj_list

    def search_recursion(self, string_search, delta_max,
                         place, all_path, verb_number, obj_list):
        branch = self.branch
        if delta_max < 0:
            return
        if verb_number >= len(all_path):
            if not branch[place].top_child_obj is None:
                obj_list.append(branch[place].top_child_obj)
            if not branch[place].curr_obj is None:
                obj_list.append(branch[place].curr_obj)
        else:
            for next_letter in branch[place].next_letters:
                if next_letter == string_search[verb_number]:
                    self.search_recursion(string_search, delta_max,
                                          branch[place].next_letters[next_letter],
                                          all_path, verb_number + 1, obj_list)
                else:
                    self.search_recursion(string_search, delta_max - 1,
                                          branch[place].next_letters[next_letter],
                                          all_path, verb_number + 1, obj_list)

    def save(self, file_name):
        file = open(file_name+".json", "w")
        for obj in self.branch:
            file.write("")
        print("tree created succesful")


class NameTreeNode:
    def __init__(self, all_path):
        self.all_path = all_path
        self.next_letters = dict()
        self.top_child_obj = None
        self.curr_obj = None

