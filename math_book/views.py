from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from .models import Subject, University, Ticket, Guest, Session, Guest_session, Vote_ticket, Theorem, Vote_theorem, Definition, Vote_definition
from django.template import loader
from django.db.models import Q
from django.urls import reverse
import random
# Create your views here.

def su_cut(string, len):
    if len(string) > len:
        string = string[0:len]
    return string

def open_account_guest(request):
    try:
        user_name = su_cut(request.COOKIES['user_name'], 40)
        session_key = su_cut(request.COOKIES['session_key'], 100)
        user = Guest.objects.get(guest_name=user_name)
        if len(Guest_session.objects.filter(session_key=session_key, guest_id=user)) == 0:
            # return HttpResponse('session inactive | user not found <br> сессия неактивна|пользователь не найден')
            user_name = 'undefined guest'
            user = Guest.objects.get(guest_name=user_name)
    except:
        user_name = 'undefined guest'
        user = Guest.objects.get(guest_name=user_name)
    return user

def sendaccountpost(request):
    try:
        type = su_cut(request.POST['registration_type'], 40)
        guest_name = su_cut(request.POST['username'], 40)
        guest_password = su_cut(request.POST['userpassword'], 40)
        if type == "new":

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
                    return HttpResponse('аккаунт не обнаружен | account not found<br>or<br>guest_information not found | информация о пользователе не найдена')
                new_user = Guest(guest_name=guest_name, guest_password=guest_password, guest_information=guest_information)
                new_user.save()
                s = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZабвгдежзийклмнопрстуфхцчшщъыьэюяАБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"


                session_key = ""
                for j in range(50):
                    session_key += s[random.randint(0, 125)]
                new_session_for_user = Guest_session(guest_id=new_user, session_key=session_key, os=os, computername=computername, HTTP_USER_AGENT=HTTP_USER_AGENT)
                new_session_for_user.save()
                template = loader.get_template('physicsesc/succesfullogin.html')
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
                if this_user.guest_password==guest_password:
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
                    s = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZабвгдежзийклмнопрстуфхцчшщъыьэюяАБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
                    session_key = ""
                    for j in range(50):
                        session_key += s[random.randint(0, 125)]
                    new_session_for_user = Guest_session(guest_id=this_user, session_key=session_key, os=os, computername=computername, HTTP_USER_AGENT=HTTP_USER_AGENT)
                    new_session_for_user.save()
                    template = loader.get_template('physicsesc/succesfullogin.html')
                    context = {
                        'user_id': this_user.id,
                        'session_key': session_key,
                        'user_name': guest_name,
                    }
                    return HttpResponse(template.render(context, request))
                else:
                    return HttpResponse('name reserved|имя занято<br><a href="/physic-in-sesc/main">main page</a>')
    except:
        return HttpResponse("server error occurred")


def send_subject(request, ):
	try:
		subject_name = su_cut(request.POST['subject_name'], 50)
		subject_description = su_cut(request.POST['subject_description'], 5000)
		picture_href = su_cut(request.POST['picture_href'], 100)
		subject = Subject(subject_name=subject_name, subject_description=subject_description, picture_href=picture_href)
		subject.save()
		subject_id = subject.id
		return HttpResponse('успешно<br><a href="/math_book/main">main page|главная страница</a><br><a href="/math_book/' + subject_id + '">show you new subject|просмотретьт ваш subject</a>')
	except:
		HttpResponse('server error<br><a href="/math_book/main">main page</a>')
def get_subject(request, subject_id):
	try:
		guest = open_account_guest(request)
		subject = Subject.objects.get(id=subject_id)
		template = loader.get_template('math_book/thisSubject.html')
		context = {
			'subject': subject,
			'color_theme': guest.color_theme,
		}
		return HttpResponse(template.render(context, request))
	except:
		return HttpResponse('sorry, it seems, it a server error')
def show_all_subject(request):
	return show_subject(request,'all')
def show_subject(request,sort_type):
	return show_subject_page(request,sort_type,1)
def show_subject_page(request,sort_type,page_number):
	try:
		guest = open_account_guest(request)
		page_number = max(1, page_number)
		subjects_list = Subject.objects.filter(task_type_private=False).order_by('-pub_date')[(page_number-1)*50:page_number*50]
		page_count = len(Subject.objects.filter(task_type_private=False))//50+1
		next_page = page_number < page_count
		template = loader.get_template('math_book/listSubject.html')
		context = {
			'subjects_list': subjects_list,
			'page_name': sort_type,
			'pages': page_number,
			'pagescount': page_count,
			'next_page': next_page,
			'pagemenu': True,
			'color_theme': guest.color_theme,
		}
		return HttpResponse(template.render(context, request))
	except:
		return HttpResponse('error')
def show_all_tickets_from_subject(request, subject_id):
	return show_tickets_from_subject(request, subject_id, 'all')
def show_tickets_from_subject(request, subject_id, sort_type):
	return show_tickets_from_subject_page(request, subject_id, sort_type, 1)
def show_tickets_from_subject_page(request, subject_id, sort_type, page_number):
	try:
		guest = open_account_guest(request)
		subject = Subject.objects.get(pk=subject_id)
		ticket_set = subject.ticket_set
		page_count = len(ticket_set)
		next_page = page_number > page_count
		tickets_list = subject.ticket_set[:100]
		template = loader.get_template('math_book/listTicket.html')
		context = {
			'tickets_list': tickets_list,
			'page_name': sort_type,
			'pages': page_number,
			'pagescount': page_count,
			'next_page': next_page,
			'pagemenu': True,
			'color_theme': guest.color_theme,
		}
		return render(request, template, context)
	except:
		return HttpResponse('server error occurred')
def show_all_theorems_from_subject(request, subject_id):
	return show_theorems_from_subject(request, subject_id, 'all')
def show_theorems_from_subject(request, subject_id, sort_type):
	return show_theorems_from_subject_page(request, subject_id, sort_type, 1)
def show_theorems_from_subject_page(request, subject_id, sort_type, page_number):
	try:
		guest = open_account_guest(request)
		subject = Subject.objects.get(pk=subject_id)
		theorem_set = subject.theorem_set
		page_count = len(theorem_set)
		next_page = page_number > page_count
		theorems_list = subject.theorem_set[:100]
		template = loader.get_template('math_book/listTheorem.html')
		context = {
			'theorems_list': theorems_list,
			'page_name': sort_type,
			'pages': page_number,
			'pagescount': page_count,
			'next_page': next_page,
			'pagemenu': True,
			'color_theme': guest.color_theme,
		}
		return render(request, template, context)
	except:
		return HttpResponse('server error occurred')
def show_all_definitions_from_subject(request, subject_id):
	return show_definitions_from_subject(request, subject_id, 'all')
def show_definitions_from_subject(request, subject_id, sort_type):
	return show_definitions_from_subject_page(request, subject_id, sort_type, 1)
def show_definitions_from_subject_page(request, subject_id, sort_type, page_number):
	try:
		guest = open_account_guest(request)
		subject = Subject.objects.get(pk=subject_id)
		definition_set = subject.definition_set
		page_count = len(definition_set)
		next_page = page_number > page_count
		definitions_list = subject.definition_set[:100]
		template = loader.get_template('math_book/listDefinition.html')
		context = {
			'definitions_list': definitions_list,
			'page_name': sort_type,
			'pages': page_number,
			'pagescount': page_count,
			'next_page': next_page,
			'pagemenu': True,
			'color_theme': guest.color_theme,
		}
		return render(request, template, context)
	except:
		return HttpResponse('server error occurred')
def create_subject(request):
	try:
		guest = open_account_guest(request)
		template = loader.get_template('math_book/create_subject.html')
		context = {
			'guest': guest,
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
		university_description = su_cut(request.POST['university_description'], 5000)
		picture_href = su_cut(request.POST['picture_href'], 100)
		university = University(university_shortname=university_shortname, university_name=university_name, university_site=university_site, university_description=university_description, picture_href=picture_href)
		university.save()
		university_id = university.id
		return HttpResponse('успешно<br><a href="/math_book/main">main page|главная страница</a><br><a href="/math_book/' + university_id + '">show you new university|просмотретьт ваш university</a>')
	except:
		HttpResponse('server error<br><a href="/math_book/main">main page</a>')
def get_university(request, university_id):
	try:
		guest = open_account_guest(request)
		university = University.objects.get(id=university_id)
		template = loader.get_template('math_book/thisUniversity.html')
		context = {
			'university': university,
			'color_theme': guest.color_theme,
		}
		return HttpResponse(template.render(context, request))
	except:
		return HttpResponse('sorry, it seems, it a server error')
def show_all_university(request):
	return show_university(request,'all')
def show_university(request,sort_type):
	return show_university_page(request,sort_type,1)
def show_university_page(request,sort_type,page_number):
	try:
		guest = open_account_guest(request)
		page_number = max(1, page_number)
		universitys_list = University.objects.filter(task_type_private=False).order_by('-pub_date')[(page_number-1)*50:page_number*50]
		page_count = len(University.objects.filter(task_type_private=False))//50+1
		next_page = page_number < page_count
		template = loader.get_template('math_book/listUniversity.html')
		context = {
			'universitys_list': universitys_list,
			'page_name': sort_type,
			'pages': page_number,
			'pagescount': page_count,
			'next_page': next_page,
			'pagemenu': True,
			'color_theme': guest.color_theme,
		}
		return HttpResponse(template.render(context, request))
	except:
		return HttpResponse('error')
def show_all_tickets_from_university(request, university_id):
	return show_tickets_from_university(request, university_id, 'all')
def show_tickets_from_university(request, university_id, sort_type):
	return show_tickets_from_university_page(request, university_id, sort_type, 1)
def show_tickets_from_university_page(request, university_id, sort_type, page_number):
	try:
		guest = open_account_guest(request)
		university = University.objects.get(pk=university_id)
		ticket_set = university.ticket_set
		page_count = len(ticket_set)
		next_page = page_number > page_count
		tickets_list = university.ticket_set[:100]
		template = loader.get_template('math_book/listTicket.html')
		context = {
			'tickets_list': tickets_list,
			'page_name': sort_type,
			'pages': page_number,
			'pagescount': page_count,
			'next_page': next_page,
			'pagemenu': True,
			'color_theme': guest.color_theme,
		}
		return render(request, template, context)
	except:
		return HttpResponse('server error occurred')
def show_all_sessions_from_university(request, university_id):
	return show_sessions_from_university(request, university_id, 'all')
def show_sessions_from_university(request, university_id, sort_type):
	return show_sessions_from_university_page(request, university_id, sort_type, 1)
def show_sessions_from_university_page(request, university_id, sort_type, page_number):
	try:
		guest = open_account_guest(request)
		university = University.objects.get(pk=university_id)
		session_set = university.session_set
		page_count = len(session_set)
		next_page = page_number > page_count
		sessions_list = university.session_set[:100]
		template = loader.get_template('math_book/listSession.html')
		context = {
			'sessions_list': sessions_list,
			'page_name': sort_type,
			'pages': page_number,
			'pagescount': page_count,
			'next_page': next_page,
			'pagemenu': True,
			'color_theme': guest.color_theme,
		}
		return render(request, template, context)
	except:
		return HttpResponse('server error occurred')
def create_university(request):
	try:
		guest = open_account_guest(request)
		template = loader.get_template('math_book/create_university.html')
		context = {
			'guest': guest,
			'color_theme': guest.color_theme,
		}
		return HttpResponse(template.render(context, request))
	except:
		return HttpResponse('error')
def send_ticket(request, university_id, subject_id):
	try:
		university = University.objects.get(id=university_id)
		subject = Subject.objects.get(id=subject_id)
		guest = open_account_guest(request)
		ticket_name = su_cut(request.POST['ticket_name'], 100)
		ticket_text = su_cut(request.POST['ticket_text'], 10000)
		study_direction = su_cut(request.POST['study_direction'], 50)
		picture_href = su_cut(request.POST['picture_href'], 100)
		vote_for_count = su_cut(request.POST['vote_for_count'], 10)
		if vote_for_count.isdigit() == False:
			vote_for_count = 0
		vote_for_count = int(vote_for_count)
		vote_against_count = su_cut(request.POST['vote_against_count'], 10)
		if vote_against_count.isdigit() == False:
			vote_against_count = 0
		vote_against_count = int(vote_against_count)
		ticket_type_private = False
		try:
			if request.POST['ticket_type_private']:
				ticket_type_private = True
			else:
				ticket_type_private = False
		except:
			ticket_type_private = False
		if len(guest.ticket_set.filter(ticket_text=ticket_text)) == 0:
			guest.ticket_set.create(university=university, subject=subject, ticket_type_private=ticket_type_private, vote_for_count=vote_for_count, vote_against_count=vote_against_count, ticket_name=ticket_name, ticket_text=ticket_text, study_direction=study_direction, picture_href=picture_href)
			ticket_id = guest.ticket_set.get(ticket_name=ticket_name).id
			return HttpResponse('успешно<br><a href="/math_book/main">main page|главная страница</a><br><a href="/math_book/' + ticket_id + '">back to ticket | обратно к ticket</a>')
		else:
			return HttpResponse('ddos attack identified and reflected <a href="//main">main page|главная страница(go fuck)</a>')
	except:
		HttpResponse('server error<br><a href="/math_book/main">main page</a>')
def get_ticket(request, ticket_id):
	try:
		guest = open_account_guest(request)
		ticket = Ticket.objects.get(id=ticket_id)
		template = loader.get_template('math_book/thisTicket.html')
		context = {
			'ticket': ticket,
			'color_theme': guest.color_theme,
		}
		return HttpResponse(template.render(context, request))
	except:
		return HttpResponse('sorry, it seems, it a server error')
def show_all_ticket(request):
	return show_ticket(request,'all')
def show_ticket(request,sort_type):
	return show_ticket_page(request,sort_type,1)
def show_ticket_page(request,sort_type,page_number):
	try:
		guest = open_account_guest(request)
		page_number = max(1, page_number)
		tickets_list = Ticket.objects.filter(task_type_private=False).order_by('-pub_date')[(page_number-1)*50:page_number*50]
		page_count = len(Ticket.objects.filter(task_type_private=False))//50+1
		next_page = page_number < page_count
		template = loader.get_template('math_book/listTicket.html')
		context = {
			'tickets_list': tickets_list,
			'page_name': sort_type,
			'pages': page_number,
			'pagescount': page_count,
			'next_page': next_page,
			'pagemenu': True,
			'color_theme': guest.color_theme,
		}
		return HttpResponse(template.render(context, request))
	except:
		return HttpResponse('error')
def create_ticket(request):
	try:
		guest = open_account_guest(request)
		template = loader.get_template('math_book/create_ticket.html')
		context = {
			'guest': guest,
			'color_theme': guest.color_theme,
		}
		return HttpResponse(template.render(context, request))
	except:
		return HttpResponse('error')
def send_vote_ticket(request, ticket_id, vote_type):
	try:
		ticket = Ticket.objects.get(id=ticket_id)
		guest = open_account_guest(request)
		if vote_type == "vote_for":
			vote_type = True
		elif vote_type == "vote_against":
			vote_type = False
		else:
			vote_type = True
			return HttpResponse("нет такого варианта голоса")
		if len(ticket.vote_ticket_set.filter(guest = guest)) <= 0:
			if vote_type == True:
				ticket.vote_for_count = ticket.vote_for_count + 1
				ticket.save()
			elif vote_type == False:
				ticket.vote_against_count = ticket.vote_against_count + 1
				ticket.save()
			vote_ticket = Vote_ticket(ticket=ticket, vote_type=vote_type, guest=guest)
			vote_ticket.save()
			template = loader.get_template('math_book/thisTicket.html')
			context = {
				'ticket': ticket,
				'color_theme': open_account_guest(request).color_theme,
			}
			return HttpResponse(template.render(context, request))
		else:
			if ticket.vote_ticket_set.get(guest=guest).vote_type == vote_type:
				template = loader.get_template('math_book/thisTicket.html')
				context = {
					'ticket': ticket,
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
			vote_ticket = ticket.vote_ticket_set.get(guest=guest)
			vote_ticket.vote_type = vote_type
			vote_ticket.save()
			template = loader.get_template('math_book/thisTicket.html')
			context = {
				'ticket': ticket,
				'color_theme': open_account_guest(request).color_theme,
			}
			return HttpResponse(template.render(context, request))
	except:
		return HttpResponse('server error occurred')
def send_session(request, university_id):
	try:
		university = University.objects.get(id=university_id)
		guest = open_account_guest(request)
		session_name = su_cut(request.POST['session_name'], 50)
		session_description = su_cut(request.POST['session_description'], 5000)
		if len(guest.session_set.filter(session_description=session_description)) == 0:
			guest.session_set.create(university=university, session_name=session_name, session_description=session_description)
			session_id = guest.session_set.get(session_name=session_name).id
			return HttpResponse('успешно<br><a href="/math_book/main">main page|главная страница</a><br><a href="/math_book/' + session_id + '">back to session | обратно к session</a>')
		else:
			return HttpResponse('ddos attack identified and reflected <a href="//main">main page|главная страница(go fuck)</a>')
	except:
		HttpResponse('server error<br><a href="/math_book/main">main page</a>')
def get_session(request, session_id):
	try:
		guest = open_account_guest(request)
		session = Session.objects.get(id=session_id)
		template = loader.get_template('math_book/thisSession.html')
		context = {
			'session': session,
			'color_theme': guest.color_theme,
		}
		return HttpResponse(template.render(context, request))
	except:
		return HttpResponse('sorry, it seems, it a server error')
def show_all_session(request):
	return show_session(request,'all')
def show_session(request,sort_type):
	return show_session_page(request,sort_type,1)
def show_session_page(request,sort_type,page_number):
	try:
		guest = open_account_guest(request)
		page_number = max(1, page_number)
		sessions_list = Session.objects.filter(task_type_private=False).order_by('-pub_date')[(page_number-1)*50:page_number*50]
		page_count = len(Session.objects.filter(task_type_private=False))//50+1
		next_page = page_number < page_count
		template = loader.get_template('math_book/listSession.html')
		context = {
			'sessions_list': sessions_list,
			'page_name': sort_type,
			'pages': page_number,
			'pagescount': page_count,
			'next_page': next_page,
			'pagemenu': True,
			'color_theme': guest.color_theme,
		}
		return HttpResponse(template.render(context, request))
	except:
		return HttpResponse('error')
def create_session(request):
	try:
		guest = open_account_guest(request)
		template = loader.get_template('math_book/create_session.html')
		context = {
			'guest': guest,
			'color_theme': guest.color_theme,
		}
		return HttpResponse(template.render(context, request))
	except:
		return HttpResponse('error')
def send_theorem(request, subject_id):
	try:
		subject = Subject.objects.get(id=subject_id)
		guest = open_account_guest(request)
		theorem_name = su_cut(request.POST['theorem_name'], 50)
		theorem_text = su_cut(request.POST['theorem_text'], 10000)
		theorem_proof = su_cut(request.POST['theorem_proof'], 10000)
		picture_href = su_cut(request.POST['picture_href'], 100)
		vote_for_count = su_cut(request.POST['vote_for_count'], 10)
		if vote_for_count.isdigit() == False:
			vote_for_count = 0
		vote_for_count = int(vote_for_count)
		vote_against_count = su_cut(request.POST['vote_against_count'], 10)
		if vote_against_count.isdigit() == False:
			vote_against_count = 0
		vote_against_count = int(vote_against_count)
		if len(guest.theorem_set.filter(theorem_text=theorem_text)) == 0:
			guest.theorem_set.create(subject=subject, vote_for_count=vote_for_count, vote_against_count=vote_against_count, theorem_name=theorem_name, theorem_text=theorem_text, theorem_proof=theorem_proof, picture_href=picture_href)
			theorem_id = guest.theorem_set.get(theorem_name=theorem_name).id
			return HttpResponse('успешно<br><a href="/math_book/main">main page|главная страница</a><br><a href="/math_book/' + theorem_id + '">back to theorem | обратно к theorem</a>')
		else:
			return HttpResponse('ddos attack identified and reflected <a href="//main">main page|главная страница(go fuck)</a>')
	except:
		HttpResponse('server error<br><a href="/math_book/main">main page</a>')
def get_theorem(request, theorem_id):
	try:
		guest = open_account_guest(request)
		theorem = Theorem.objects.get(id=theorem_id)
		template = loader.get_template('math_book/thisTheorem.html')
		context = {
			'theorem': theorem,
			'color_theme': guest.color_theme,
		}
		return HttpResponse(template.render(context, request))
	except:
		return HttpResponse('sorry, it seems, it a server error')
def show_all_theorem(request):
	return show_theorem(request,'all')
def show_theorem(request,sort_type):
	return show_theorem_page(request,sort_type,1)
def show_theorem_page(request,sort_type,page_number):
	try:
		guest = open_account_guest(request)
		page_number = max(1, page_number)
		theorems_list = Theorem.objects.filter(task_type_private=False).order_by('-pub_date')[(page_number-1)*50:page_number*50]
		page_count = len(Theorem.objects.filter(task_type_private=False))//50+1
		next_page = page_number < page_count
		template = loader.get_template('math_book/listTheorem.html')
		context = {
			'theorems_list': theorems_list,
			'page_name': sort_type,
			'pages': page_number,
			'pagescount': page_count,
			'next_page': next_page,
			'pagemenu': True,
			'color_theme': guest.color_theme,
		}
		return HttpResponse(template.render(context, request))
	except:
		return HttpResponse('error')
def create_theorem(request):
	try:
		guest = open_account_guest(request)
		template = loader.get_template('math_book/create_theorem.html')
		context = {
			'guest': guest,
			'color_theme': guest.color_theme,
		}
		return HttpResponse(template.render(context, request))
	except:
		return HttpResponse('error')
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
		if len(theorem.vote_theorem_set.filter(guest = guest)) <= 0:
			if vote_type == True:
				theorem.vote_for_count = theorem.vote_for_count + 1
				theorem.save()
			elif vote_type == False:
				theorem.vote_against_count = theorem.vote_against_count + 1
				theorem.save()
			vote_theorem = Vote_theorem(theorem=theorem, vote_type=vote_type, guest=guest)
			vote_theorem.save()
			template = loader.get_template('math_book/thisTheorem.html')
			context = {
				'theorem': theorem,
				'color_theme': open_account_guest(request).color_theme,
			}
			return HttpResponse(template.render(context, request))
		else:
			if theorem.vote_theorem_set.get(guest=guest).vote_type == vote_type:
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
			vote_theorem = theorem.vote_theorem_set.get(guest=guest)
			vote_theorem.vote_type = vote_type
			vote_theorem.save()
			template = loader.get_template('math_book/thisTheorem.html')
			context = {
				'theorem': theorem,
				'color_theme': open_account_guest(request).color_theme,
			}
			return HttpResponse(template.render(context, request))
	except:
		return HttpResponse('server error occurred')
def send_definition(request, subject_id):
	try:
		subject = Subject.objects.get(id=subject_id)
		guest = open_account_guest(request)
		definition_name = su_cut(request.POST['definition_name'], 50)
		definition_text = su_cut(request.POST['definition_text'], 10000)
		picture_href = su_cut(request.POST['picture_href'], 100)
		vote_for_count = su_cut(request.POST['vote_for_count'], 10)
		if vote_for_count.isdigit() == False:
			vote_for_count = 0
		vote_for_count = int(vote_for_count)
		vote_against_count = su_cut(request.POST['vote_against_count'], 10)
		if vote_against_count.isdigit() == False:
			vote_against_count = 0
		vote_against_count = int(vote_against_count)
		if len(guest.definition_set.filter(definition_text=definition_text)) == 0:
			guest.definition_set.create(subject=subject, vote_for_count=vote_for_count, vote_against_count=vote_against_count, definition_name=definition_name, definition_text=definition_text, picture_href=picture_href)
			definition_id = guest.definition_set.get(definition_name=definition_name).id
			return HttpResponse('успешно<br><a href="/math_book/main">main page|главная страница</a><br><a href="/math_book/' + definition_id + '">back to definition | обратно к definition</a>')
		else:
			return HttpResponse('ddos attack identified and reflected <a href="//main">main page|главная страница(go fuck)</a>')
	except:
		HttpResponse('server error<br><a href="/math_book/main">main page</a>')
def get_definition(request, definition_id):
	try:
		guest = open_account_guest(request)
		definition = Definition.objects.get(id=definition_id)
		template = loader.get_template('math_book/thisDefinition.html')
		context = {
			'definition': definition,
			'color_theme': guest.color_theme,
		}
		return HttpResponse(template.render(context, request))
	except:
		return HttpResponse('sorry, it seems, it a server error')
def show_all_definition(request):
	return show_definition(request,'all')
def show_definition(request,sort_type):
	return show_definition_page(request,sort_type,1)
def show_definition_page(request,sort_type,page_number):
	try:
		guest = open_account_guest(request)
		page_number = max(1, page_number)
		definitions_list = Definition.objects.filter(task_type_private=False).order_by('-pub_date')[(page_number-1)*50:page_number*50]
		page_count = len(Definition.objects.filter(task_type_private=False))//50+1
		next_page = page_number < page_count
		template = loader.get_template('math_book/listDefinition.html')
		context = {
			'definitions_list': definitions_list,
			'page_name': sort_type,
			'pages': page_number,
			'pagescount': page_count,
			'next_page': next_page,
			'pagemenu': True,
			'color_theme': guest.color_theme,
		}
		return HttpResponse(template.render(context, request))
	except:
		return HttpResponse('error')
def create_definition(request):
	try:
		guest = open_account_guest(request)
		template = loader.get_template('math_book/create_definition.html')
		context = {
			'guest': guest,
			'color_theme': guest.color_theme,
		}
		return HttpResponse(template.render(context, request))
	except:
		return HttpResponse('error')
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
		if len(definition.vote_definition_set.filter(guest = guest)) <= 0:
			if vote_type == True:
				definition.vote_for_count = definition.vote_for_count + 1
				definition.save()
			elif vote_type == False:
				definition.vote_against_count = definition.vote_against_count + 1
				definition.save()
			vote_definition = Vote_definition(definition=definition, vote_type=vote_type, guest=guest)
			vote_definition.save()
			template = loader.get_template('math_book/thisDefinition.html')
			context = {
				'definition': definition,
				'color_theme': open_account_guest(request).color_theme,
			}
			return HttpResponse(template.render(context, request))
		else:
			if definition.vote_definition_set.get(guest=guest).vote_type == vote_type:
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
			vote_definition = definition.vote_definition_set.get(guest=guest)
			vote_definition.vote_type = vote_type
			vote_definition.save()
			template = loader.get_template('math_book/thisDefinition.html')
			context = {
				'definition': definition,
				'color_theme': open_account_guest(request).color_theme,
			}
			return HttpResponse(template.render(context, request))
	except:
		return HttpResponse('server error occurred')

