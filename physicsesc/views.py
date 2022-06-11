from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from .models import Task, Solution, Guest, Usefulfiles, Guest_session, Like, Report, Vote
from django.template import loader
from django.urls import reverse
import random
def su_cut(string, l):
    if len(string) > l:
        string = string[0:l]
    return string
def index(request):
    try:

        latest_tasks_list = Task.objects.all()[:1]

        #task.task_text="hi for all. you in my project fizhub, where you can post your physic tasks"
        template = loader.get_template('physicsesc/fizhub.html')
        context = {
            'latest_tasks_list': latest_tasks_list,
        }
        # antiddos(request=request)
        return HttpResponse((template.render(context, request)))
    except:
        return HttpResponse('<a href="/physic-in-sesc/main">main page</a>')
def main(request):
    return main_page(request,1)
def main_page(request,page_number):
    page_number = max(1,page_number)
    latest_tasks_list = Task.objects.all()[(page_number-1)*50:page_number*50]
    page_count = len(Task.objects.all())//50+1
    next_page = page_number < page_count
    template = loader.get_template('physicsesc/fizhub.html')
    context = {
        'latest_tasks_list': latest_tasks_list,
        'page_name': 'main',
        'pages': page_number,
        'pagescount': page_count,
        'next_page': next_page
    }
    #antiddos(request=request)
    return HttpResponse((template.render(context, request)))
def new(request):

    return new_page(request, 1)
def new_page(request, page_number):
    page_number = max(1, page_number)
    latest_tasks_list = Task.objects.order_by('-pub_date')[(page_number-1)*50:page_number*50]
    page_count = len(Task.objects.all())//50+1
    next_page = page_number < page_count
    template = loader.get_template('physicsesc/fizhub.html')
    context = {
        'latest_tasks_list': latest_tasks_list,
        'page_name': 'new',
        'pages': page_number,
        'pagescount': page_count,
        'next_page': next_page
    }
    return HttpResponse(template.render(context, request))
def best(request):

    return best_page(request, 1)
def best_page(request, page_number):
    page_number = max(1, page_number)
    latest_tasks_list = (Task.objects.order_by('like')[::-1])[(page_number-1)*50:page_number*50]
    page_count = len(Task.objects.all())//50+1
    next_page = page_number < page_count
    template = loader.get_template('physicsesc/fizhub.html')
    context = {
        'latest_tasks_list': latest_tasks_list,
        'page_name': 'best',
        'pages': page_number,
        'pagescount': page_count,
        'next_page': next_page
    }
    return HttpResponse(template.render(context, request))
def theme(request):
    return render(request, 'physicsesc/theme.html')
def themepost(request):
    theme1_name = request.POST['theme1']
    theme2_name = request.POST['theme2']
    latest_tasks_list = Task.objects.filter(theme1_name=theme1_name)
    if theme2_name!="No theme":
        latest_tasks_list = latest_tasks_list.filter(theme2_name=theme2_name)
    template = loader.get_template('physicsesc/fizhub.html')
    context = {
        'latest_tasks_list': latest_tasks_list,
    }
    return HttpResponse(template.render(context, request))
def themefind(request,theme_name1):
    latest_tasks_list = Task.objects.filter(theme1_name=theme_name1)[:40]
    template = loader.get_template('physicsesc/fizhub.html')
    context = {
        'latest_tasks_list': latest_tasks_list,
    }
    return HttpResponse(template.render(context, request))
def themefind2(request,theme_name1,theme_name2):
    latest_tasks_list = Task.objects.filter(theme1_name=theme_name1, theme2_name=theme_name2)[:40]
    template = loader.get_template('physicsesc/fizhub.html')
    context = {
        'latest_tasks_list': latest_tasks_list,
    }
    return HttpResponse(template.render(context, request))
def user(request):

    return render(request, 'physicsesc/userfind.html')
def userfind(request,user_name):
    try:
        latest_tasks_list = Guest.objects.get(guest_name=user_name).task_set.all()

        page_number = 1
        page_count = len(latest_tasks_list) // 50 + 1
        next_page = page_number < page_count
        template = loader.get_template('physicsesc/fizhub.html')
        context = {
            'latest_tasks_list': latest_tasks_list,
            'page_name': 'user/'+user_name,
            'pages': page_number,
            'pagescount': page_count,
            'next_page': next_page
        }
        return HttpResponse(template.render(context, request))
    except:
        return HttpResponse('server error<br><a href="/physic-in-sesc/main">main page</a>')
def userfind_page(request,user_name):
    try:
        latest_tasks_list = Guest.objects.get(guest_name=user_name).task_set.all()

        page_number = 1
        page_count = len(latest_tasks_list) // 50 + 1
        next_page = page_number < page_count
        template = loader.get_template('physicsesc/fizhub.html')
        context = {
            'latest_tasks_list': latest_tasks_list,
            'page_name': 'best',
            'pages': page_number,
            'pagescount': page_count,
            'next_page': next_page
        }
        return HttpResponse(template.render(context, request))
    except:
        return HttpResponse('server error<br><a href="/physic-in-sesc/main">main page</a>')

def login(request):
    return render(request, 'physicsesc/login.html')
def sendaccount(request, guest_name,guest_password):
    #try:
    if (len(Guest.objects.filter(guest_name=guest_name)))==0:
        new_user = Guest(guest_name=guest_name,guest_password=guest_password)
        new_user.save()
        return HttpResponse('you user_id is '+str(new_user.id))
    else:
        this_user = Guest.objects.get(guest_name=guest_name)
        if this_user.guest_password==guest_password:
            return HttpResponse('you user_id is ' + str(this_user.id))
    return HttpResponse('name reserved|имя занято<br><a href="/physic-in-sesc/main">main page</a>')
    #except:
        #raise Http404("Error")

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
        return HttpResponse("server error")
def task(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")
    return render(request, 'physicsesc/thistask.html', {'task': task})
def like(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
        try:
            user_name = su_cut(request.COOKIES['user_name'], 40)
            session_key = su_cut(request.COOKIES['session_key'], 100)
            user = Guest.objects.get(guest_name=user_name)
            if len(Guest_session.objects.filter(session_key=session_key, guest_id=user))==0:
                return HttpResponse('session inactive | user not found <br> сессия неактивна|пользователь не найден')
        except:
            return HttpResponse('session inactive | user not found <br> сессия неактивна|пользователь не найден')
        user = Guest.objects.get(guest_name=user_name)
        if len(task.like_set.filter(guest=user))<=0:
            if len(task.report_set.filter(guest=user)) >0:
                task.report_count=task.report_count-1
                report=Report.objects.get(task=task, guest=user)
                report.delete()
            task.like_count=task.like_count+1
            task.save()
            like = Like(task=task, guest=user)
            like.save()

        else:
            return render(request, 'physicsesc/thistask.html', {'task': task, 'alert': 'вы уже оценили эту задачу'})


    except Task.DoesNotExist:
        raise Http404("Task does not exist")
    return render(request, 'physicsesc/thistask.html', {'task': task})
def report(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
        try:
            user_name = su_cut(request.COOKIES['user_name'], 40)
            session_key = su_cut(request.COOKIES['session_key'], 100)
            user = Guest.objects.get(guest_name=user_name)
            if len(Guest_session.objects.filter(session_key=session_key, guest_id=user)) == 0:
                return HttpResponse('session inactive | user not found <br> сессия неактивна|пользователь не найден')
        except:

            return HttpResponse('session inactive | user not found <br> сессия неактивна|пользователь не найден')
        user = Guest.objects.get(guest_name=user_name)
        if len(task.report_set.filter(guest=user))<=0:
            if len(task.like_set.filter(guest=user)) >0:
                task.like_count=task.like_count-1
                like=Like.objects.get(task=task, guest=user)
                like.delete()
            task.report_count=task.report_count+1
            task.save()
            report = Report(task=task, guest=user)
            report.save()
        else:
            return render(request, 'physicsesc/thistask.html', {'task': task, 'alert': 'вы уже оценили эту задачу'})

    except Task.DoesNotExist:
        raise Http404("Task does not exist")
    return render(request, 'physicsesc/thistask.html', {'task': task})
def solution(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
        solution_set = Solution.objects.filter(task=task.id).order_by('-votes_count', 'votes_against_count')[:100]

        #solution = Solution.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")
    return render(request, 'physicsesc/thissolution.html', {'task': task,'solution_set':solution_set})
def solution_vote(request, task_id, solution_id, vote_type):
    try:
        task = Task.objects.get(pk=task_id)
        solution_set = Solution.objects.filter(task=task.id)[:100]
        solution = Solution.objects.get(task=task.id, id=solution_id)
        try:
            user_name = su_cut(request.COOKIES['user_name'], 40)

            session_key = su_cut(request.COOKIES['session_key'], 100)
            user = Guest.objects.get(guest_name=user_name)
            if len(Guest_session.objects.filter(session_key=session_key, guest_id=user)) == 0:
                return HttpResponse('session inactive | user not found <br> сессия неактивна|пользователь не найден')
        except:
            return HttpResponse('session inactive | user not found <br> сессия неактивна|пользователь не найден')
        user = Guest.objects.get(guest_name=user_name)
        if vote_type == "vote_for":
            vote_type = True
        elif vote_type == "vote_against":
            vote_type = False
        else:
            return HttpResponse("нет такого варианта голоса")
        if len(solution.vote_set.filter(guest=user)) <= 0:
            if vote_type==True:
                solution.votes_count = solution.votes_count + 1
                solution.save()
            elif vote_type == False:
                solution.votes_against_count = solution.votes_against_count + 1
                solution.save()
            vote = Vote(task=task, solution=solution, vote_type=vote_type, guest=user)
            vote.save()
            return render(request, 'physicsesc/thissolution.html', {'task': task, 'solution_set': solution_set})
        else:
            if solution.vote_set.get(guest=user).vote_type == vote_type:
                return render(request, 'physicsesc/thissolution.html', {'task': task, 'solution_set': solution_set, 'alert': 'вы уже так оценили эту задачу'})
            else:
                if vote_type == True:
                    solution.votes_against_count = solution.votes_against_count - 1
                    solution.votes_count = solution.votes_count + 1
                    solution.save()
                elif vote_type == False:
                    solution.votes_count = solution.votes_count - 1
                    solution.votes_against_count = solution.votes_against_count + 1
                    solution.save()

            vote = solution.vote_set.get(guest=user)
            vote.vote_type = vote_type
            vote.save()
            return render(request, 'physicsesc/thissolution.html', {'task': task, 'solution_set': solution_set})


        #solution = Solution.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")
    return render(request, 'physicsesc/thissolution.html', {'task': task, 'solution_set': solution_set})

def makesolution(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")
    return render(request, 'physicsesc/makesolution.html', {'task': task})
def makesolution3(request, task_id, solution_text):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")
    #task.solution_set.solution_text=solution_text

    task.solution_set.create(solution_text=solution_text)

    #print(task.solution_set.solution_text)

    return HttpResponse('<a href="/physic-in-sesc/main">main page</a>')
def sendsolutionpost(request):
    try:
        try:
            user_name = su_cut(request.COOKIES['user_name'], 40)

            session_key = su_cut(request.COOKIES['session_key'], 100)
            user = Guest.objects.get(guest_name=user_name)
            if len(Guest_session.objects.filter(session_key=session_key, guest_id=user)) == 0:
                return HttpResponse('session inactive | user not found <br> сессия неактивна|пользователь не найден')
        except:
            return HttpResponse('session inactive | user not found <br> сессия неактивна | пользователь не найден')

        task_id = su_cut(request.POST['taskid'], 100)
        solution_text = su_cut(request.POST['solutiontext'], 500)
        task = Task.objects.get(pk=task_id)
        if len(task.solution_set.filter(solution_text=solution_text))==0 and len(solution_text)>=5:
            task.solution_set.create(solution_text=solution_text, creator_id=user)
            return HttpResponse('успешно<br><a href="/physic-in-sesc/main">main page|главная страница</a><br><a href="/physic-in-sesc/'+task_id+'">back to task|обратно к задаче</a>')
        else:
            return HttpResponse('ddos attack identified and reflected <a href="/physic-in-sesc/main">main page|главная страница(go fuck)</a>')
    except:
        return HttpResponse('server error<br><a href="/physic-in-sesc/main>main page</a>')
"""def makesolution2(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    try:
        selected_solution = task.solution_set.get(pk=request.POST['solution'])
    except (KeyError, Solution.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'physicsesc/fizhub.html', {
            'task': task,
            'error_message': "You didn't select a solution.",
        })
    else:
        selected_solution.solution_text += 1
        selected_solution.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('physic-in-sesc:solution', args=(task.id,)))
"""
def createtask(request):
        return render(request, 'physicsesc/createtask.html')
def sendtaskpost(request):
    try:
        t=1
        try:
            user_name = su_cut(request.COOKIES['user_name'], 40)
            session_key = su_cut(request.COOKIES['session_key'], 100)
            user = Guest.objects.get(guest_name=user_name)
            if len(Guest_session.objects.filter(session_key=session_key, guest_id=user))==0:
                return HttpResponse('session inactive | user not found <br> сессия неактивна|пользователь не найден')
        except:
            user_name = 'undefined guest'
            user = Guest.objects.get(guest_name=user_name)

        task_name=su_cut(request.POST['taskheader'], 50)
        task_text=su_cut(request.POST['textarea'], 1500)
        theme1_name = su_cut(request.POST['theme1'], 30)
        theme2_name = su_cut(request.POST['theme2'], 30)
        picture_url=su_cut(request.POST['pictureurl'], 100)
        if len(task_text)>=10 and len(task_name)>2 and task_name.count(" ")<len(task_name):
            if user.guest_rights==0:
                user.task_set.create(task_name=task_name,task_text=task_text, pub_date=timezone.now(),picture_href=picture_url, theme1_name=theme1_name, theme2_name=theme2_name)
                #taskid= user.task_set.all()[-1:-2]
                return HttpResponse('succesful <br> <a href="/physic-in-sesc/new">last tasks</a>')
            elif user.guest_rights>=1:
                try:
                    userfile = request.FILES['file']
                    filesize= userfile.size
                    if filesize>100 and filesize<3000000:
                        fs = FileSystemStorage()
                        filename = fs.save(user_name+"_"+userfile.name, userfile)
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

        return HttpResponse("password incorrect or недостаточная длина условия или названия задачи")
    except:
        return HttpResponse('server error<br><a href="/physic-in-sesc/main">main page</a>')
"""
def sendtask(request, task_text,theme1_name, theme2_name, creator_name,creator_password):
    try:
        user = Guest.objects.get(guest_name=creator_name)
        if user.guest_password==creator_password:
            #task = Task(task_text=task_text, pub_date=timezone.now(), theme1_name=theme1_name, theme2_name=theme2_name, creator_name=creator_name)
            user.task_set.create(task_text=task_text, pub_date=timezone.now(), theme1_name=theme1_name, theme2_name=theme2_name)
            #print(task.solution_set.solution_text)
            return HttpResponse('succesful <br> <a href="physic-in-sesc/main>main page</a>')
    except:
        HttpResponse('server error<br><a href="physic-in-sesc/main>main page</a>')
def sendtaskwithpicture(request, task_text,picture_url,theme1_name, theme2_name, creator_name,creator_password):
    try:
        user = Guest.objects.get(guest_name=creator_name)
        if user.guest_password==creator_password:
            picture_url=picture_url.replace("^","/")
            #task = Task(task_text=task_text, pub_date=timezone.now(), theme1_name=theme1_name, theme2_name=theme2_name, creator_name=creator_name)
            user.task_set.create(task_text=task_text, pub_date=timezone.now(), theme1_name=theme1_name, theme2_name=theme2_name,picture_href=picture_url)
            #print(task.solution_set.solution_text)
            return HttpResponse('succesful <br> <a href="physic-in-sesc/main>main page</a>')
    except:
        return HttpResponse('server error<br><a href="physic-in-sesc/main>main page</a>')
"""
def useful(request):
    useful_files = Usefulfiles.objects.all()[:50]
    template=loader.get_template('physicsesc/useful.html')
    context = {
        'useful_files': useful_files,
    }
    return HttpResponse(template.render(context,request))
def sendusefulfile(request):
    try:
        filename = su_cut(request.POST['filename'], 50)
        username = su_cut(request.POST['username'], 40)
        userpassword = su_cut(request.POST['userpassword'], 40)
        filehref = su_cut(request.POST['filehref'], 200)
        user = (Guest.objects.get(guest_name=username))
        if user.guest_password==userpassword and filename!="" and filehref!="":
            file = user.usefulfiles_set.create(file_name=filename,file_href=filehref)
            file.save()

            return HttpResponse('succesful')
        else:
            return HttpResponse('not succesful')
    except:
        return HttpResponse('server error<br><a href="/physic-in-sesc/main">main page</a>')

def account(request,user_name):
    user_name_request = user_name
    user_request = Guest.objects.get(guest_name=user_name_request)
    try:
        user = openaccount(request)
        if user.id == user_request.id:
            return myaccount(request)
    except:
        user = '1'


    template = loader.get_template('physicsesc/user.html')
    tasks_count = len(user_request.task_set.all())
    context = {
        'tasks_count': tasks_count,
        'user': user_request,

    }
    return HttpResponse(template.render(context,request))
def myaccount(request):
    try:
        user = openaccount(request)
        template = loader.get_template('physicsesc/user.html')
        tasks_count = len(user.task_set.all())
        context = {
            'tasks_count': tasks_count,
            'user': user,
            'its_me': True

        }
        return HttpResponse(template.render(context,request))
    except:
        return HttpResponse('сессия недействительна')


def settings(request):
    try:
        user = openaccount(request)
        if user.guest_name=='undefined guest':
            return HttpResponse('войдите сначала в свой аккаунт')
        template = loader.get_template('physicsesc/settings.html')
        sessions = user.guest_session_set.all()
        session_key = su_cut(request.COOKIES['session_key'], 100)
        context = {
        'session_key': session_key,
        'sessions': sessions,
        'user': user,
        'its_me': True

        }
        return HttpResponse(template.render(context,request))
    except:
        return HttpResponse('сессия недействительна')
def closesession(request, session_key):
    try:
        user = openaccount(request)
        if len(user.guest_session_set.all().filter(session_key=session_key))>0:
            session = user.guest_session_set.all().get(session_key=session_key)
            session.delete()

        user = openaccount(request)
        template = loader.get_template('physicsesc/settings.html')
        sessions = user.guest_session_set.all()
        session_key = su_cut(request.COOKIES['session_key'], 100)
        context = {
        'session_key': session_key,
        'sessions': sessions,
        'user': user,
        'its_me': True

        }
        return HttpResponse(template.render(context,request))
    except:
        return HttpResponse('сессия недействительна')
def changeaccountinformation(request):
    try:
        user = openaccount(request)
        if user=="undefined guest":
            return HttpResponse('сессия недействительна')
        guest_information = su_cut(request.POST['guest_information'], 2000)
        if user.guest_information != guest_information:
            user.guest_information = guest_information
            user.save()
        return settings(request)
    except:
        return HttpResponse('сессия недействительна')
def changepassword(request):
    try:
        user = openaccount(request)
        if user == "undefined guest":
            return HttpResponse('сессия недействительна')
        old_password = su_cut(request.POST['old_password'], 40)
        new_password = su_cut(request.POST['new_password'], 40)
        if user.guest_password == old_password:
            user.guest_password = new_password
            user.save()
        return settings(request)
    except:
        return HttpResponse('сессия недействительна')
def openaccount(request):
    try:
        user_name = su_cut(request.COOKIES['user_name'], 40)
        session_key = su_cut(request.COOKIES['session_key'], 100)
        user = Guest.objects.get(guest_name=user_name)
        if len(Guest_session.objects.filter(session_key=session_key, guest_id=user)) == 0:
            return HttpResponse('session inactive | user not found <br> сессия неактивна|пользователь не найден')
    except:
        user_name = 'undefined guest'
        user = Guest.objects.get(guest_name=user_name)
    return user
def antiddos(request):
    print(request.META.HTTP_COOKIE)
