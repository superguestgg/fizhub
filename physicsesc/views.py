from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from .models import Task, Solution, Guest, Usefulfiles, Guest_session, Like, Report, Vote, Olympiad, Olympiad_part, Olympiad_task, Group, Group_student, Group_author_helper, Group_theme, Group_task, Article, Article_vote, Article_page
from django.template import loader
from django.db.models import Q
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
    template = loader.get_template('physicsesc/fizhubmain.html')
    context = {}
    return HttpResponse(template.render(context,request))
def main_page(request,page_number):
    page_number = max(1,page_number)
    latest_tasks_list = Task.objects.filter(task_type_private=False)[(page_number-1)*50:page_number*50]
    page_count = len(Task.objects.filter(task_type_private=False))//50+1
    next_page = page_number < page_count
    template = loader.get_template('physicsesc/fizhub.html')
    context = {
        'latest_tasks_list': latest_tasks_list,
        'page_name': 'main',
        'pages': page_number,
        'pagescount': page_count,
        'next_page': next_page,
        'pagemenu': True,
    }
    #antiddos(request=request)
    return HttpResponse((template.render(context, request)))
def maintask(request):
    return maintask_page(request,1)
def maintask_page(request,page_number):
    page_number = max(1,page_number)
    latest_tasks_list = Task.objects.filter(task_type_private=False)[(page_number-1)*50:page_number*50]
    page_count = len(Task.objects.filter(task_type_private=False))//50+1
    next_page = page_number < page_count
    template = loader.get_template('physicsesc/fizhub.html')
    context = {
        'latest_tasks_list': latest_tasks_list,
        'page_name': 'main',
        'pages': page_number,
        'pagescount': page_count,
        'next_page': next_page,
        'pagemenu': True,
    }
    #antiddos(request=request)
    return HttpResponse((template.render(context, request)))
def new(request):

    return new_page(request, 1)
def new_page(request, page_number):
    page_number = max(1, page_number)
    latest_tasks_list = Task.objects.filter(task_type_private=False).order_by('-pub_date')[(page_number-1)*50:page_number*50]
    page_count = len(Task.objects.filter(task_type_private=False))//50+1
    next_page = page_number < page_count
    template = loader.get_template('physicsesc/fizhub.html')
    context = {
        'latest_tasks_list': latest_tasks_list,
        'page_name': 'new',
        'pages': page_number,
        'pagescount': page_count,
        'next_page': next_page,
        'pagemenu': True,
    }
    return HttpResponse(template.render(context, request))
def best(request):

    return best_page(request, 1)
def best_page(request, page_number):
    page_number = max(1, page_number)
    latest_tasks_list = (Task.objects.filter(task_type_private=False).order_by('-like_count'))[(page_number-1)*50:page_number*50]
    page_count = len(Task.objects.filter(task_type_private=False))//50+1
    next_page = page_number < page_count
    template = loader.get_template('physicsesc/fizhub.html')
    context = {
        'latest_tasks_list': latest_tasks_list,
        'page_name': 'best',
        'pages': page_number,
        'pagescount': page_count,
        'next_page': next_page,
        'pagemenu': True,
    }
    return HttpResponse(template.render(context, request))
def my(request):
    return my_page(request,1)
def my_page(request, page_number):
    user = openaccount(request)
    page_number = max(1, page_number)
    latest_tasks_list = (Task.objects.filter(creator_name=user))[(page_number-1)*50:page_number*50]
    page_count = len(Task.objects.all())//50+1
    next_page = page_number < page_count
    template = loader.get_template('physicsesc/fizhub.html')
    context = {
        'latest_tasks_list': latest_tasks_list,
        'page_name': 'best',
        'pages': page_number,
        'pagescount': page_count,
        'next_page': next_page,
        'pagemenu': True,
    }
    return HttpResponse(template.render(context, request))
def theme(request):
    return render(request, 'physicsesc/theme.html')
def themepost(request):
    theme1_name = request.POST['theme1']
    theme2_name = request.POST['theme2']
    latest_tasks_list = Task.objects.filter(task_type_private=False).filter(theme1_name=theme1_name)
    if theme2_name!="No theme":
        latest_tasks_list = latest_tasks_list.filter(theme2_name=theme2_name)
    template = loader.get_template('physicsesc/fizhub.html')
    context = {
        'latest_tasks_list': latest_tasks_list,
    }
    return HttpResponse(template.render(context, request))
def themefind(request,theme_name1):
    latest_tasks_list = Task.objects.filter(task_type_private=False).filter(theme1_name=theme_name1)[:40]
    template = loader.get_template('physicsesc/fizhub.html')
    context = {
        'latest_tasks_list': latest_tasks_list,
    }
    return HttpResponse(template.render(context, request))
def themefind2(request,theme_name1,theme_name2):
    latest_tasks_list = Task.objects.filter(task_type_private=False).filter(theme1_name=theme_name1, theme2_name=theme_name2)[:40]
    template = loader.get_template('physicsesc/fizhub.html')
    context = {
        'latest_tasks_list': latest_tasks_list,
    }
    return HttpResponse(template.render(context, request))
def classfind(request,class_name):
    latest_tasks_list = Task.objects.filter(task_type_private=False).filter(class_name=class_name)[:40]
    template = loader.get_template('physicsesc/fizhub.html')
    context = {
        'latest_tasks_list': latest_tasks_list,
    }
    return HttpResponse(template.render(context, request))
def user(request):

    return render(request, 'physicsesc/userfind.html')
def userfind(request,user_name):
    try:
        latest_tasks_list = Guest.objects.get(guest_name=user_name).task_set.filter(task_type_private=False)

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
        latest_tasks_list = Guest.objects.get(guest_name=user_name).task_set.filter(task_type_private=False)

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
    return HttpResponse('name reserved|?????? ????????????<br><a href="/physic-in-sesc/main">main page</a>')
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
                    return HttpResponse('?????????????? ???? ?????????????????? | account not found<br>or<br>guest_information not found | ???????????????????? ?? ???????????????????????? ???? ??????????????')
                new_user = Guest(guest_name=guest_name, guest_password=guest_password, guest_information=guest_information)
                new_user.save()
                s = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????"


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
                return HttpResponse('?????? ???????????? | name reserved')

        else:
            if (len(Guest.objects.filter(guest_name=guest_name))) == 0:
                return HttpResponse('?????????????? ???? ?????????????????? | account not found<br>or<br>guest_information not found')
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
                    s = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????"
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
                    return HttpResponse('name reserved|?????? ????????????<br><a href="/physic-in-sesc/main">main page</a>')
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
                return HttpResponse('session inactive | user not found <br> ???????????? ??????????????????|???????????????????????? ???? ????????????')
        except:
            return HttpResponse('session inactive | user not found <br> ???????????? ??????????????????|???????????????????????? ???? ????????????')
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
            return render(request, 'physicsesc/thistask.html', {'task': task, 'alert': '???? ?????? ?????????????? ?????? ????????????'})


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
                return HttpResponse('session inactive | user not found <br> ???????????? ??????????????????|???????????????????????? ???? ????????????')
        except:

            return HttpResponse('session inactive | user not found <br> ???????????? ??????????????????|???????????????????????? ???? ????????????')
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
            return render(request, 'physicsesc/thistask.html', {'task': task, 'alert': '???? ?????? ?????????????? ?????? ????????????'})

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
        solution_set = Solution.objects.filter(task=task.id).order_by('-votes_count', 'votes_against_count')[:100]
        solution = Solution.objects.get(task=task.id, id=solution_id)
        try:
            user_name = su_cut(request.COOKIES['user_name'], 40)

            session_key = su_cut(request.COOKIES['session_key'], 100)
            user = Guest.objects.get(guest_name=user_name)
            if len(Guest_session.objects.filter(session_key=session_key, guest_id=user)) == 0:
                return HttpResponse('session inactive | user not found <br> ???????????? ??????????????????|???????????????????????? ???? ????????????')
        except:
            return HttpResponse('session inactive | user not found <br> ???????????? ??????????????????|???????????????????????? ???? ????????????')
        user = Guest.objects.get(guest_name=user_name)
        if vote_type == "vote_for":
            vote_type = True
        elif vote_type == "vote_against":
            vote_type = False
        else:
            return HttpResponse("?????? ???????????? ???????????????? ????????????")
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
                return render(request, 'physicsesc/thissolution.html', {'task': task, 'solution_set': solution_set, 'alert': '???? ?????? ?????? ?????????????? ?????? ????????????'})
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
                return HttpResponse('session inactive | user not found <br> ???????????? ??????????????????|???????????????????????? ???? ????????????')
        except:
            return HttpResponse('session inactive | user not found <br> ???????????? ?????????????????? | ???????????????????????? ???? ????????????')

        task_id = su_cut(request.POST['taskid'], 100)
        solution_text = su_cut(request.POST['solutiontext'], 500)
        task = Task.objects.get(pk=task_id)
        if len(task.solution_set.filter(solution_text=solution_text))==0 and len(solution_text)>=5:
            task.solution_set.create(solution_text=solution_text, creator_id=user)
            return HttpResponse('??????????????<br><a href="/physic-in-sesc/main">main page|?????????????? ????????????????</a><br><a href="/physic-in-sesc/'+task_id+'">back to task|?????????????? ?? ????????????</a>')
        else:
            return HttpResponse('ddos attack identified and reflected <a href="/physic-in-sesc/main">main page|?????????????? ????????????????(go fuck)</a>')
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
                return HttpResponse('session inactive | user not found <br> ???????????? ??????????????????|???????????????????????? ???? ????????????')
        except:
            user_name = 'undefined guest'
            user = Guest.objects.get(guest_name=user_name)

        task_name=su_cut(request.POST['taskheader'], 50)
        task_text=su_cut(request.POST['textarea'], 3000)
        theme1_name = su_cut(request.POST['theme1'], 30)
        theme2_name = su_cut(request.POST['theme2'], 30)
        class_name = su_cut(str(request.POST['class_name']), 10)
        if class_name.isdigit()==False:
            class_name=11
        class_name=int(class_name)
        class_name=min(max(class_name, 7), 100)
        try:
            if request.POST['task_type_private']:
                task_type_private = True
            else:
                task_type_private = False
        except:
            task_type_private = False
        picture_url=su_cut(request.POST['pictureurl'], 100)
        if len(task_text)>=10 and len(task_name)>2 and task_name.count(" ")<len(task_name):
            if user.guest_rights==0:
                user.task_set.create(task_name=task_name,task_text=task_text, pub_date=timezone.now(),picture_href=picture_url, theme1_name=theme1_name, theme2_name=theme2_name, class_name=class_name, task_type_private=task_type_private)
                task_id=user.task_set.get(task_name=task_name).id
                #taskid= user.task_set.all()[-1:-2]
                return HttpResponse('succesful <br> <a href="/physic-in-sesc/new">last tasks</a><br><a href="/fizhub/'+str(task_id)+'">your task</a>')
            elif user.guest_rights>=1:
                try:
                    userfile = request.FILES['file']
                    filesize= userfile.size
                    if filesize>100 and filesize<3000000:
                        fs = FileSystemStorage()
                        filename = fs.save(user_name+"_"+userfile.name, userfile)
                        uploaded_file_url = fs.url(filename)
                        user.task_set.create(task_name=task_name, task_text=task_text, pub_date=timezone.now(),picture_href=uploaded_file_url, theme1_name=theme1_name, theme2_name=theme2_name, class_name=class_name, task_type_private=task_type_private)
                        user.guest_rights=user.guest_rights-1
                        task_id = user.task_set.get(task_name=task_name).id
                        user.save()
                        return HttpResponse(
                            'succesful <br> <a href="/physic-in-sesc/new">last tasks</a><br><a href="/fizhub/' + str(
                                task_id) + '">your task</a>')
                    elif  filesize>=3000000:
                        return HttpResponse('picture size too big<a href="/physic-in-sesc/main">main page</a>')
                    elif filesize>0:
                        return HttpResponse('picture size not enough big<a href="/physic-in-sesc/main">main page</a>')
                    else:

                        user.task_set.create(task_name=task_name, task_text=task_text, pub_date=timezone.now(), picture_href=picture_url, theme1_name=theme1_name, theme2_name=theme2_name, class_name=class_name, task_type_private=task_type_private)
                        task_id = user.task_set.get(task_name=task_name).id
                        return HttpResponse(
                            'succesful <br> <a href="/physic-in-sesc/new">last tasks</a><br><a href="/fizhub/' + str(
                                task_id) + '">your task</a>')
                except:
                    user.task_set.create(task_name=task_name, task_text=task_text, pub_date=timezone.now(), picture_href=picture_url, theme1_name=theme1_name, theme2_name=theme2_name, class_name=class_name, task_type_private=task_type_private)
                    task_id = user.task_set.get(task_name=task_name).id
                    return HttpResponse(
                        'succesful <br> <a href="/physic-in-sesc/new">last tasks</a><br><a href="/fizhub/' + str(
                            task_id) + '">your task</a>')

        return HttpResponse("password incorrect or ?????????????????????????? ?????????? ?????????????? ?????? ???????????????? ????????????")
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

def account(request, user_name):
    user_name_request = user_name
    user_request = Guest.objects.get(guest_name=user_name_request)
    try:
        user = openaccount(request)
        if user.id == user_request.id:
            return myaccount(request)
    except:
        user = '1'

    if len(user.subscription_set.filter(author_id=user_request.id))>0:
        subscription = True
    else:
        subscription = False
    template = loader.get_template('physicsesc/user.html')
    tasks_count = len(user_request.task_set.all())
    context = {
        'tasks_count': tasks_count,
        'user': user_request,
        'subscription': subscription,
    }
    return HttpResponse(template.render(context,request))
def makesubscribe(request, user_name):
    user_name_request = user_name
    user_request = Guest.objects.get(guest_name=user_name_request)
    try:
        user = openaccount(request)
        if user.id == user_request.id:
            return myaccount(request)
    except:
        user = '1'
    if user.guest_name == 'undefined guest':
        return HttpResponse('?????????????? ?????????????? ?? ???????? ??????????????')
    template = loader.get_template('physicsesc/user.html')
    tasks_count = len(user_request.task_set.all())
    if len(user.subscription_set.filter(author_id=user_request.id))==0:
        user.subscription_set.create(author_id=user_request.id)
        user.subscription_count = user.subscription_count + 1
        user.save()
        user_request.subscriber_count = user_request.subscriber_count + 1
        user_request.save()
        context = {
            'tasks_count': tasks_count,
            'user': user_request,
            'subscription': True,
        }
    else:
        context = {
            'tasks_count': tasks_count,
            'user': user_request,
            'alert': '???? ?????? ?????????????????? ???? ?????????? ????????????????????????',
            'subscription': True,

        }
    return HttpResponse(template.render(context,request))
def unsubscribe(request, user_name):
    user_name_request = user_name
    user_request = Guest.objects.get(guest_name=user_name_request)
    try:
        user = openaccount(request)
        if user.id == user_request.id:
            return myaccount(request)
    except:
        user = '1'
    if user.guest_name == 'undefined guest':
        return HttpResponse('?????????????? ?????????????? ?? ???????? ??????????????')
    template = loader.get_template('physicsesc/user.html')
    tasks_count = len(user_request.task_set.all())
    if len(user.subscription_set.filter(author_id=user_request.id))>0:
        subscription=user.subscription_set.get(author_id=user_request.id)
        subscription.delete()
        user.subscription_count = user.subscription_count - 1
        user.save()
        user_request.subscriber_count = user_request.subscriber_count - 1
        user_request.save()
        context = {
            'tasks_count': tasks_count,
            'user': user_request,
            'subscription': False,

        }
    else:
        context = {
            'tasks_count': tasks_count,
            'user': user_request,
            'alert': '???? ???? ?????????????????? ???? ?????????? ????????????????????????',
            'subscription': False,

        }
    return HttpResponse(template.render(context,request))
def subscribes(request):
    return subscribes_page(request,1)
def subscribes_page(request,page_number):
    if True:
        page_number = max(1, page_number)
        user = openaccount(request)
        if user.guest_name=='undefined guest':
            return HttpResponse('?????????????? ?????????????? ?? ???????? ??????????????')
        template = loader.get_template('physicsesc/subscribes.html')

        subscriptions = user.subscription_set.all()[50*(page_number-1):50*page_number]
        page_count = len(subscriptions) // 50 + 1
        next_page = page_number < page_count
        authors_id_list = []
        for subscription in subscriptions:
            authors_id_list.append(subscription.author_id)
        authors_list = Guest.objects.filter(id__in = authors_id_list)
        context = {
            'authors_list': authors_list,
            'pages': page_number,
            'next_page': next_page,
            'page_name': 'subscribes',
            'pagescount': page_count,
        }

        return HttpResponse(template.render(context, request))
    else:
        return HttpResponse('???????????? ??????????????????????????????')

def myaccount(request):
    try:
        user = openaccount(request)

        template = loader.get_template('physicsesc/user.html')

        tasks_count = len(user.task_set.all())

        subscriptions = user.subscription_set.all()[:100]

        for subscription in subscriptions:

            subscription.author_id = Guest.objects.get(id=subscription.author_id).guest_name

        context = {
            'tasks_count': tasks_count,
            'user': user,
            'its_me': True,
            'subscriptions': subscriptions,

        }
        return HttpResponse(template.render(context, request))
    except:
        return HttpResponse('???????????? ??????????????????????????????')


def settings(request):
    try:
        user = openaccount(request)
        if user.guest_name=='undefined guest':
            return HttpResponse('?????????????? ?????????????? ?? ???????? ??????????????')
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
        return HttpResponse('???????????? ??????????????????????????????')
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
        return HttpResponse('???????????? ??????????????????????????????')
def changeaccountinformation(request):
    try:
        user = openaccount(request)
        if user=="undefined guest":
            return HttpResponse('???????????? ??????????????????????????????')
        guest_information = su_cut(request.POST['guest_information'], 2000)
        if user.guest_information != guest_information:
            user.guest_information = guest_information
            user.save()
        return settings(request)
    except:
        return HttpResponse('???????????? ??????????????????????????????')
def changepassword(request):
    try:
        user = openaccount(request)
        if user == "undefined guest":
            return HttpResponse('???????????? ??????????????????????????????')
        old_password = su_cut(request.POST['old_password'], 40)
        new_password = su_cut(request.POST['new_password'], 40)
        if user.guest_password == old_password:
            user.guest_password = new_password
            user.save()
        return settings(request)
    except:
        return HttpResponse('???????????? ??????????????????????????????')

def olympiad(request):
    return olympiad_page(request, 1)
def olympiad_page(request, page_number):
    user = openaccount(request)
    page_number = max(1,page_number)
    olympiad_list = Olympiad.objects.all()[(page_number-1)*50:page_number*50]
    page_count = len(olympiad_list)//50+1
    next_page = page_number < page_count
    template = loader.get_template('physicsesc/olympiad.html')
    context = {
        'olympiad_list': olympiad_list,
        'page_name': 'olympiad',
        'pages': page_number,
        'pagescount': page_count,
        'next_page': next_page
    }
    #antiddos(request=request)
    return HttpResponse((template.render(context, request)))


def all_group(request):
    return all_group_page(request, 1)
def all_group_page(request, page_number):
    user = openaccount(request)
    page_number = max(1, page_number)
    group_list = Group.objects.filter(group_private_type=False)[(page_number-1)*50:page_number*50]
    page_count = len(group_list)//50+1
    next_page = page_number < page_count
    template = loader.get_template('physicsesc/group.html')
    context = {
        'group_list': group_list,
        'page_name': 'group',
        'pages': page_number,
        'pagescount': page_count,
        'next_page': next_page
    }
    #antiddos(request=request)
    return HttpResponse((template.render(context, request)))


def new_group(request):
    return new_group_page(request, 1)
def new_group_page(request, page_number):
    user = openaccount(request)
    page_number = max(1, page_number)
    group_list = Group.objects.filter(group_private_type=False)[(page_number-1)*50:page_number*50:-1]
    page_count = len(group_list)//50+1
    next_page = page_number < page_count
    template = loader.get_template('physicsesc/group.html')
    context = {
        'group_list': group_list,
        'page_name': 'group/new',
        'pages': page_number,
        'pagescount': page_count,
        'next_page': next_page
    }
    #antiddos(request=request)
    return HttpResponse((template.render(context, request)))
def popular_group(request):
    return popular_group_page(request, 1)
def popular_group_page(request, page_number):
    user = openaccount(request)
    page_number = max(1, page_number)
    group_list = Group.objects.filter(group_private_type=False).order_by('-student_count')[(page_number-1)*50:page_number*50]
    page_count = len(group_list)//50+1
    next_page = page_number < page_count
    template = loader.get_template('physicsesc/group.html')
    context = {
        'group_list': group_list,
        'page_name': 'group/popular',
        'pages': page_number,
        'pagescount': page_count,
        'next_page': next_page
    }
    #antiddos(request=request)
    return HttpResponse((template.render(context, request)))
def creategroup(request):
    user = openaccount(request)
    if user.guest_name == "undefined guest":
        return HttpResponse('?????????????? ?????????????? ?? ???????? ??????????????')
    template = loader.get_template('physicsesc/creategroup.html')
    context = {
        'page_name': 'creategroup',
    }
    #antiddos(request=request)
    return HttpResponse((template.render(context, request)))
def sendgrouppost(request):
    if True:
        user=openaccount(request)
        t=0
        if user.guest_name=="undefined guest":
            return HttpResponse('?????????????? ?????????????? ?? ???????? ??????????????')
        user_name=user.guest_name
        group_name=su_cut(request.POST['taskheader'], 50)
        group_description=su_cut(request.POST['textarea'], 3000)
        group_password = su_cut(request.POST['taskheader'], 50)
        try:
            if request.POST['group_type_password']:
                group_type_password = True
            else:
                group_type_password = False
        except:
            group_type_password = False
        try:
            if request.POST['group_private_type']:
                group_private_type = True
            else:
                group_private_type = False
        except:
            group_private_type = False
        try:
            if request.POST['group_application_type']:
                group_application_type = True
            else:
                group_application_type = False
        except:
            group_application_type = False
        picture_url=su_cut(request.POST['pictureurl'], 100)
        if len(group_description)>=10 and len(group_name)>2 and group_name.count(" ")<len(group_name):
            if user.guest_rights==0:
                user.group_set.create(group_name=group_name,group_description=group_description, picture_href=picture_url, group_type_password=group_type_password, group_password=group_password, group_private_type=group_private_type, group_application_type=group_application_type)
                group_id=user.group_set.get(group_name=group_name).id
                group = Group.objects.get(id=group_id)
                group.group_theme_set.create(group_theme_name='main')
                #taskid= user.task_set.all()[-1:-2]
                return HttpResponse('succesful <br> <a href="/physic-in-sesc/new">last tasks</a><br><a href="/fizhub/group/'+str(group_id)+'">your group</a>')
            elif user.guest_rights>=1:
                try:
                    userfile = request.FILES['file']
                    filesize= userfile.size
                    if filesize>100 and filesize<3000000:
                        fs = FileSystemStorage()
                        filename = fs.save(user_name+"_"+userfile.name, userfile)
                        uploaded_file_url = fs.url(filename)
                        user.group_set.create(group_name=group_name, group_description=group_description, picture_href=uploaded_file_url, group_type_password=group_type_password, group_password=group_password, group_private_type=group_private_type, group_application_type=group_application_type)
                        user.guest_rights=user.guest_rights-1
                        group_id = user.group_set.get(group_name=group_name).id
                        group = Group.objects.get(id=group_id)
                        group.group_theme_set.create(group_theme_name='main')
                        user.save()
                        return HttpResponse(
                            'succesful <br> <a href="/physic-in-sesc/new">last tasks</a><br><a href="/fizhub/group/' + str(
                                group_id) + '">your group</a>')
                    elif  filesize>=3000000:
                        return HttpResponse('picture size too big<a href="/physic-in-sesc/main">main page</a>')
                    elif filesize>0:
                        return HttpResponse('picture size not enough big<a href="/physic-in-sesc/main">main page</a>')
                    else:

                        user.group_set.create(group_name=group_name, group_description=group_description, picture_href=picture_url, group_type_password=group_type_password, group_password=group_password, group_private_type=group_private_type, group_application_type=group_application_type)
                        group_id = user.group_set.get(group_name=group_name).id
                        group = Group.objects.get(id=group_id)
                        group.group_theme_set.create(group_theme_name='main')
                        return HttpResponse(
                            'succesful <br> <a href="/physic-in-sesc/new">last tasks</a><br><a href="/fizhub/group/' + str(
                                group_id) + '">your group</a>')
                except:
                    user.group_set.create(group_name=group_name, group_description=group_description, picture_href=picture_url, group_type_password=group_type_password, group_password=group_password, group_private_type=group_private_type, group_application_type=group_application_type)
                    group_id = user.group_set.get(group_name=group_name).id
                    group = Group.objects.get(id=group_id)
                    group.group_theme_set.create(group_theme_name='main')
                    return HttpResponse(
                        'succesful <br> <a href="/physic-in-sesc/new">last tasks</a><br><a href="/fizhub/group/' + str(
                            group_id) + '">your group</a>')

        return HttpResponse("password incorrect or ?????????????????????????? ?????????? ?????????????? ?????? ???????????????? ????????????")
    else:
        return HttpResponse('server error<br><a href="/physic-in-sesc/main">main page</a>')
def groupfind(request):
    return HttpResponse('later.........')
def my_group(request):
    return my_group_page(request, 1)
def my_group_page(request, page_number):
    user = openaccount(request)
    if user.guest_name == "undefined guest":
        return HttpResponse('?????????????? ?????????????? ?? ???????? ??????????????')
    page_number = max(1, page_number)
    group_list = Group.objects.filter(group_private_type=False, author=user)[(page_number-1)*50:page_number*50]
    page_count = len(group_list)//50+1
    next_page = page_number < page_count
    template = loader.get_template('physicsesc/group.html')
    context = {
        'group_list': group_list,
        'page_name': 'group/my',
        'pages': page_number,
        'pagescount': page_count,
        'next_page': next_page
    }
    #antiddos(request=request)
    return HttpResponse((template.render(context, request)))

def student_group(request):
    return student_group_page(request, 1)
def student_group_page(request, page_number):
    user = openaccount(request)
    if user.guest_name == "undefined guest":
        return HttpResponse('?????????????? ?????????????? ?? ???????? ??????????????')
    page_number = max(1, page_number)
    group_student_list = user.group_student_set.filter(application_type=True)
    group_id_list = []
    for group_student in group_student_list:
        group_id_list.append(group_student.group.id)
    group_list = Group.objects.filter(id__in=group_id_list)[(page_number-1)*50:page_number*50]
    page_count = len(group_list)//50+1
    next_page = page_number < page_count
    template = loader.get_template('physicsesc/group.html')
    context = {
        'group_list': group_list,
        'page_name': 'group/student',
        'pages': page_number,
        'pagescount': page_count,
        'next_page': next_page
    }
    #antiddos(request=request)
    return HttpResponse((template.render(context, request)))

def thisgroup(request, group_id):
    return group_page(request, group_id, 1)
def group_page(request, group_id, page_number):
    user = openaccount(request)
    if user.guest_name == "undefined guest":
        return HttpResponse('?????????????? ?????????????? ?? ???????? ??????????????')
    page_number=max(1, page_number)
    group = Group.objects.get(id=group_id)
    opengroup1 = opengroup(user, group_id)

    if opengroup1 in ['student', 'author', 'helper']:
        group_task_list = group.group_task_set.all()
        group_task_list_id = []
        for group_task in group_task_list:
            group_task_list_id.append(group_task.task.id)
        task_list = Task.objects.filter(id__in=group_task_list_id)
        page_count = len(task_list)//50+1
        task_list = task_list[50*(page_number-1):50*page_number]
        next_page = (page_count > page_number)
        template = loader.get_template('physicsesc/thisgroup.html')
        context = {
            'is_author': (opengroup1=='author'),
            'is_helper': (opengroup1=='helper'),
            'group': group,
            'task_list': task_list,
            'page_name': 'group/'+str(group.id),
            'pages': page_number,
            'pagescount': page_count,
            'next_page': next_page
        }
        return HttpResponse(template.render(context,request))
    elif opengroup1=='no':
        return creategroupapplication(request, group_id)
    elif opengroup1=='application':
        return HttpResponse('???? ???????????? ???????????? ?? ?????? ????????????')
    else:
        return HttpResponse('???? ???????????? ???????????? ?? ?????? ????????????')
def creategrouptask(request, group_id):
    user = openaccount(request)
    if user.guest_name == "undefined guest":
        return HttpResponse('?????????????? ?????????????? ?? ???????? ??????????????')


    group = Group.objects.get(id=group_id)

    opengroup1 = opengroup(user, group_id)

    if opengroup1 in ['author', 'helper']:

        themes = group.group_theme_set.all()
        template = loader.get_template('physicsesc/creategrouptask.html')
        context = {
            'themes': themes,
            'is_author': (opengroup1=='author'),
            'is_helper': (opengroup1=='helper'),
            'group': group,
            'page_name': '???????????????? ??????????????'
        }

        return HttpResponse(template.render(context, request))
    elif opengroup1 == 'student':
        return HttpResponse('???????????? ???? ?????????? ?????????????????? ????????????')
    elif opengroup1 == 'no':
        return creategroupapplication(request, group_id)
    elif opengroup1 == 'application':
        return HttpResponse('???? ???????????? ???????????? ?? ?????? ????????????')
    else:
        return HttpResponse('???? ???????????? ???????????? ?? ?????? ????????????')
def sendgrouptaskpost(request):
    if True:
        user = openaccount(request)
        t = 0
        if user.guest_name == "undefined guest":
            return HttpResponse('?????????????? ?????????????? ?? ???????? ??????????????')
        user_name = user.guest_name
        task_id = su_cut(str(request.POST['task_id']), 10)
        group_id = su_cut(request.POST['group_id'], 10)
        if task_id.isdigit()==False:
            return HttpResponse('???? ?? ?????? ??????, ??????????')
        if group_id.isdigit()==False:
            return HttpResponse('???? ?? ?????? ??????, ??????????')
        task_id = int(task_id)
        group_id = int(group_id)
        group = Group.objects.get(id=group_id)
        task = Task.objects.get(id=task_id)

        task_comment = su_cut(request.POST['task_comment'], 3000)
        group_theme = su_cut(request.POST['group_theme'], 50)

        theme = group.group_theme_set.get(group_theme_name=group_theme)
        theme.task_count = theme.task_count+1
        group.group_task_set.create(group_theme=theme, task_comment=task_comment, task=task)

        return group_page(request, group_id, 1)
    else:
        return HttpResponse('server error<br><a href="/physic-in-sesc/main">main page</a>')
def grouptheme(request,group_id):
    return grouptheme_page(request,group_id, 1)
def grouptheme_page(request, group_id, page_number):
    user = openaccount(request)
    if user.guest_name == "undefined guest":
        return HttpResponse('?????????????? ?????????????? ?? ???????? ??????????????')
    page_number=max(1, page_number)
    group = Group.objects.get(id=group_id)
    opengroup1 = opengroup(user, group_id)
    if opengroup1 in ['author', 'helper', 'student']:
        group_theme_list = group.group_theme_set.all()
        theme_list = group_theme_list
        page_count = len(theme_list)//50+1
        theme_list = theme_list[50*(page_number-1):50*page_number]
        next_page = (page_count > page_number)
        template = loader.get_template('physicsesc/thisgrouptheme.html')
        context = {
            'is_author': (opengroup1=='author'),
            'is_helper': (opengroup1=='helper'),
            'group': group,
            'theme_list': theme_list,
            'page_name': 'group/'+str(group.id)+'/theme',
            'pages': page_number,
            'pagescount': page_count,
            'next_page': next_page
        }
        return HttpResponse(template.render(context,request))
    elif opengroup1=='no':
        return creategroupapplication(request, group_id)

def creategrouptheme(request, group_id):
    user = openaccount(request)
    if user.guest_name == "undefined guest":
        return HttpResponse('?????????????? ?????????????? ?? ???????? ??????????????')


    group = Group.objects.get(id=group_id)
    opengroup1 = opengroup(user, group_id)
    if opengroup1 in ['author', 'helper']:

        themes = group.group_theme_set.all()
        template = loader.get_template('physicsesc/creategrouptheme.html')
        context = {
            'themes': themes,
            'is_author': (opengroup1=='author'),
            'is_helper': (opengroup1=='helper'),
            'group': group,
            'page_name': '???????????????? ????????'
        }

        return HttpResponse(template.render(context, request))
    elif opengroup1 == 'student':
        return HttpResponse('???????????? ???? ?????????? ?????????????????? ????????')
    elif opengroup1=='no':
        return creategroupapplication(request, group_id)
def sendgroupthemepost(request):
    if True:
        user = openaccount(request)
        t = 0
        if user.guest_name == "undefined guest":
            return HttpResponse('?????????????? ?????????????? ?? ???????? ??????????????')
        user_name = user.guest_name
        group_theme_name = su_cut(str(request.POST['group_theme_name']), 50)
        group_theme_description = su_cut(request.POST['group_theme_description'], 3000)
        group_id = su_cut(request.POST['group_id'], 10)
        if group_id.isdigit()==False:
            return HttpResponse('???? ?? ?????? ??????, ??????????')
        group_id = int(group_id)
        if opengroup(user, group_id) in ['author', 'helper']:
            group = Group.objects.get(id=group_id)
            if len(group.group_theme_set.filter(group_theme_name=group_theme_name))>0:
                return HttpResponse('???????????? ???????? ?????? ????????????????????')
            group.group_theme_set.create(group_theme_name=group_theme_name, group_theme_description=group_theme_description)
            group.group_theme_count = group.group_theme_count + 1
            group.save()
            return group_page(request, group_id, 1)
        else:
            return HttpResponse('?? ?????? ?????? ????????')
    else:
        return HttpResponse('server error<br><a href="/physic-in-sesc/main">main page</a>')

def groupthemetask(request, group_id, theme_name):
    return groupthemetask_page(request, group_id, theme_name, 1)
def groupthemetask_page(request, group_id, theme_name, page_number):
    user = openaccount(request)
    if user.guest_name == "undefined guest":
        return HttpResponse('?????????????? ?????????????? ?? ???????? ??????????????')
    page_number = max(1, page_number)
    group = Group.objects.get(id=group_id)
    opengroup1 = opengroup(user, group_id)
    if len(group.group_theme_set.filter(group_theme_name=theme_name))>0:
        theme = group.group_theme_set.get(group_theme_name=theme_name)
    else:
        return HttpResponse("???????? ???? ??????????????")
    if opengroup1 in ['student', 'author', 'helper']:
        group_task_list = group.group_task_set.filter(group_theme=theme)
        group_task_list_id = []
        for group_task in group_task_list:
            group_task_list_id.append(group_task.task.id)
        task_list = Task.objects.filter(id__in=group_task_list_id)
        page_count = len(task_list)//50+1
        task_list = task_list[50*(page_number-1):50*page_number]
        next_page = (page_count > page_number)
        template = loader.get_template('physicsesc/thisgroup.html')
        context = {
            'is_author': (opengroup1=='author'),
            'is_helper': (opengroup1=='helper'),
            'group': group,
            'task_list': task_list,
            'page_name': 'group/'+str(group.id)+"/theme/"+str(theme_name),
            'pages': page_number,
            'pagescount': page_count,
            'next_page': next_page
        }
        return HttpResponse(template.render(context,request))
    elif opengroup1=='no':
        return creategroupapplication(request, group_id)
    elif opengroup1=='application':
        return HttpResponse('???? ???????????? ???????????? ?? ?????? ????????????')
    else:
        return HttpResponse('??????')


def creategroupapplication(request, group_id):
    user = openaccount(request)
    group = Group.objects.get(id=group_id)
    template = loader.get_template('physicsesc/creategroupapplication.html')
    context = {
        'group': group,


    }
    return HttpResponse(template.render(context, request))
def sendgroupapplicationpost(request):
    user = openaccount(request)
    t = 0
    if user.guest_name == "undefined guest":
        return HttpResponse('?????????????? ?????????????? ?? ???????? ??????????????')
    user_name = user.guest_name
    group_id = su_cut(request.POST['group_id'], 10)
    if group_id.isdigit() == False:
        return HttpResponse('???? ?? ?????? ??????, ??????????')
    group_id = int(group_id)
    group = Group.objects.get(id=group_id)
    if len(group.group_student_set.filter(student=user))>0:
        return HttpResponse('???? ?????? ???????????? ???????????? ?? ?????? ????????????')
    if group.group_type_password == True:
        group_password = su_cut(request.POST['group_password'], 50)
        if group_password == group.group_password:
            t=1
        else:
            return HttpResponse('???????????? ????????????????, ........')
    else:
        t=1
    if t==1:
        if group.group_application_type==False:
            group.group_student_set.create(student=user, application_type=True)
            group.student_count = group.student_count + 1
            group.save()
        elif group.group_application_type==True:
            group.group_student_set.create(student=user, application_type=False)
            return HttpResponse('???????????? ?????????????? ??????????????')
    return group_page(request, group_id, 1)
def groupapplication(request, group_id):
    user = openaccount(request)
    opengroup1 = opengroup(user, group_id)
    group = Group.objects.get(id=group_id)
    if opengroup1 in ['author', 'helper']:
        applications_student = group.group_student_set.filter(application_type=False)[:100]
        applications_helper = group.group_author_helper_set.filter(application_type=False)[:100]
        template = loader.get_template('physicsesc/groupapplication.html')
        context = {

            'is_author': (opengroup1=='author'),
            'is_helper': (opengroup1=='helper'),
            'group': group,
            'page_name': '????????????',
            'applications_helper': applications_helper,
            'applications_student': applications_student,
        }
        return HttpResponse(template.render(context, request))
    elif opengroup1 == 'student':
        return HttpResponse('???????? ???????????? ?????? ????????????????????(???? ???????????? ?? ???? ???????????? ?????????????????????????? ????????????)')
    elif opengroup1 == 'application':
        return HttpResponse('???????? ???????????? ?????? ???? ????????????????')
    elif opengroup1 == 'no':
        return creategroupapplication(request, group_id)
def approvegroupapplication(request, group_id, user_name, approve_type):
    user=openaccount(request)
    user_request = Guest.objects.get(guest_name=user_name)
    group = Group.objects.get(id=group_id)
    opengroup1 = opengroup(user, group_id)
    if opengroup1 in ['author', 'helper']:
        alert = '???????????? ??????????????'
        if approve_type == 'studentaccept':
            if group.group_student_set.filter(student = user_request, application_type=False):
                alert = '??????????????'
                group.student_count = group.student_count + 1
                group.save()
                application = group.group_student_set.get(student=user_request)
                application.application_type = True
                application.save()
        elif approve_type == 'studentdelete':
            if group.group_student_set.filter(student = user_request):
                alert='??????????????'
                application = group.group_student_set.get(student=user_request)
                if application.application_type == True:
                    group.student_count = group.student_count - 1
                    group.save()
                application.delete()

        elif approve_type == 'helperaccept':
            if group.group_author_helper_set.filter(author_helper = user_request, application_type=False):
                alert = '??????????????'
                group.author_helper_count = group.author_helper_count + 1
                group.save()
                application = group.group_author_helper_set.get(author_helper=user_request)
                application.application_type = True
                application.save()
        elif approve_type == 'helperdelete':
            if group.group_author_helper_set.filter(author_helper = user_request):
                alert='??????????????'
                application = group.group_author_helper_set.get(author_helper=user_request)
                if application.application_type == True:
                    group.author_helper_count = group.author_helper_count - 1
                    group.save()
                application.delete()
        else:
            alert = '???????????????? ???? ????????????????????'
        applications_student = group.group_student_set.filter(application_type=False)[:100]
        applications_helper = group.group_author_helper_set.filter(application_type=False)[:100]
        template = loader.get_template('physicsesc/groupapplication.html')
        context = {

            'is_author': (opengroup1 == 'author'),
            'is_helper': (opengroup1 == 'helper'),
            'group': group,
            'alert': alert,
            'page_name': '????????????',
            'applications_helper': applications_helper,
            'applications_student': applications_student,
        }
        return HttpResponse(template.render(context, request))
    elif opengroup1 == 'student':
        return HttpResponse('?? ?????? ?????? ????????')
    elif opengroup1 == 'application':
        return HttpResponse('?? ?????? ?????? ????????')
    elif opengroup1 == 'no':
        return HttpResponse('?? ?????? ?????? ????????')


def groupparticipant(request, group_id):
    user = openaccount(request)
    opengroup1 = opengroup(user, group_id)
    group = Group.objects.get(id=group_id)
    if opengroup1 in ['author', 'helper']:
        participant_student = group.group_student_set.filter(application_type=True)[:100]
        if opengroup1 == 'author':
            participant_helper = group.group_author_helper_set.filter(application_type=True)[:100]
        else:
            participant_helper = False
        template = loader.get_template('physicsesc/groupparticipant.html')
        context = {

            'is_author': (opengroup1=='author'),
            'is_helper': (opengroup1=='helper'),
            'group': group,
            'page_name': '??????????????????',
            'participant_student': participant_student,
            'participant_helper': participant_helper,
        }
        return HttpResponse(template.render(context, request))
    elif opengroup1 == 'student':
        return HttpResponse('???????? ???????????? ?????? ????????????????????(???? ???????????? ?? ???? ???????????? ?????????????????????????? ????????????????????)')
    elif opengroup1 == 'application':
        return HttpResponse('???????? ???????????? ?????? ???? ????????????????')
    elif opengroup1 == 'no':
        return HttpResponse('?? ?????? ?????? ????????')
def approvegroupparticipant(request, group_id, user_name, approve_type):
    user = openaccount(request)
    user_request = Guest.objects.get(guest_name=user_name)
    group = Group.objects.get(id=group_id)
    opengroup1 = opengroup(user, group_id)
    if opengroup1 in ['author', 'helper']:
        alert = '???????????? ??????????????'
        if approve_type == 'studentaccept':
            if group.group_student_set.filter(student = user_request, application_type=False):
                alert = '??????????????'
                group.student_count = group.student_count + 1
                group.save()
                application = group.group_student_set.get(student=user_request)
                application.application_type = True
                application.save()
        elif approve_type == 'studentdelete':
            if group.group_student_set.filter(student = user_request):
                alert = '??????????????'
                application = group.group_student_set.get(student=user_request)
                if application.application_type == True:
                    group.student_count = group.student_count - 1
                    group.save()
                application.delete()

        elif approve_type == 'helperaccept':
            if group.group_author_helper_set.filter(author_helper = user_request, application_type=False):
                alert = '??????????????'
                group.author_helper_count = group.author_helper_count + 1
                group.save()
                application = group.group_author_helper_set.get(author_helper=user_request)
                application.application_type = True
                application.save()
        elif approve_type == 'helperdelete':
            if group.group_author_helper_set.filter(author_helper = user_request):
                alert='??????????????'
                application = group.group_author_helper_set.get(author_helper=user_request)
                if application.application_type == True:
                    group.author_helper_count = group.author_helper_count - 1
                    group.save()
                application.delete()
        else:
            alert = '???????????????? ???? ????????????????????'
        participant_student = group.group_student_set.filter(application_type=True)[:100]
        if opengroup1 == 'author':
            participant_helper = group.group_author_helper_set.filter(application_type=True)[:100]
        else:
            participant_helper = False
        template = loader.get_template('physicsesc/groupparticipant.html')
        context = {

            'is_author': (opengroup1=='author'),
            'is_helper': (opengroup1=='helper'),
            'group': group,
            'alert': alert,
            'page_name': '??????????????????',
            'participant_student': participant_student,
            'participant_helper': participant_helper,
        }
        return HttpResponse(template.render(context, request))
    elif opengroup1 == 'student':
        return HttpResponse('?? ?????? ?????? ????????')
    elif opengroup1 == 'application':
        return HttpResponse('?? ?????? ?????? ????????')
    elif opengroup1 == 'no':
        return HttpResponse('?? ?????? ?????? ????????')

def livephysics(request):
    user = openaccount(request)
    return HttpResponse('??....., ???? ?? ....')
    template = loader.get_template('physicsesc/livephysics.html')
    context = {}

    return HttpResponse(template.render(context, request))

def articles1(request):
    return articles(request, 'main')
def articles(request, page_name):
    return articles_page(request, page_name, 1)
def articles_page(request, page_name, page_number):
    user = openaccount(request)
    page_number = max(1, page_number)
    if page_name == 'main':
        articles_list = Article.objects.filter(article_private_type=False)[(page_number - 1) * 50:page_number * 50]
    elif page_name == 'best':
        articles_list = Article.objects.filter(article_private_type=False).order_by('-article_vote_count', 'article_vote_against_count')[(page_number - 1) * 50:page_number * 50]
    elif page_name == 'new':
        articles_list = Article.objects.filter(article_private_type=False)[(page_number - 1) * 50:page_number * 50]
        articles_list = articles_list[::-1]
    elif page_name == 'my':
        articles_list = Article.objects.filter(article_private_type=False, author=user)[(page_number - 1) * 50:page_number * 50]
    else:
        return HttpResponse('???????????? ???? ??????????????????, ?????? ??????..')
    page_count = len(Article.objects.filter(article_private_type=False)) // 50 + 1
    next_page = page_number < page_count
    template = loader.get_template('physicsesc/articles.html')
    context = {
        'articles_list': articles_list,
        'page_name': 'articles/'+page_name,
        'pages': page_number,
        'pagescount': page_count,
        'next_page': next_page,
        'pagemenu': True,
    }
    # antiddos(request=request)
    return HttpResponse((template.render(context, request)))
def articletheme(request, theme_name):
    return articletheme_page(request, theme_name, 1)
def articletheme_page(request, theme_name, page_number):
    user = openaccount(request)
    page_number = max(1, page_number)
    articles_list = Article.objects.filter(article_private_type=False).filter(Q(article_theme1_name=theme_name) | Q(article_theme2_name=theme_name))
    page_count = len(Article.objects.filter(article_private_type=False)) // 50 + 1
    next_page = page_number < page_count
    template = loader.get_template('physicsesc/articles.html')
    context = {
        'articles_list': articles_list,
        'page_name': 'articles/theme/'+theme_name,
        'pages': page_number,
        'pagescount': page_count,
        'next_page': next_page,
        'pagemenu': True,
    }
    # antiddos(request=request)
    return HttpResponse((template.render(context, request)))
def createarticle(request):
    template = loader.get_template('physicsesc/createarticle.html')
    page_name = 'createarticle'
    context = {
        'page_name': 'articles/' + page_name,
        'pagemenu': True,
    }
    return HttpResponse(template.render(context, request))

def sendarticlepost(request):
    user = openaccount(request)
    t = 0
    if user.guest_name == "undefined guest":
        return HttpResponse('?????????????? ?????????????? ?? ???????? ??????????????')
    user_name = user.guest_name
    try:
        article_private_type = request.POST['article_private_type']
        article_private_type = True
    except:
        article_private_type = False
    article_name = request.POST['article_name']
    article_theme1_name = request.POST['article_theme1_name']
    article_theme2_name = request.POST['article_theme2_name']
    article_description = request.POST['article_description']
    article_page_count = str(request.POST['pagecount'])
    if article_page_count.isdigit():
        article_page_count = int(article_page_count)
    else:
        return HttpResponse('server error')
    article = Article(author=user, article_name=article_name, article_theme1_name=article_theme1_name, article_theme2_name=article_theme2_name, article_page_count=article_page_count, article_private_type=article_private_type, article_description=article_description)
    article.save()
    for i in range (1, article_page_count+1):
        article_page_name = request.POST['article_page_name_'+str(i)]
        article_page_text = request.POST['article_page_text_' + str(i)]
        article.article_page_set.create(article_page_name=article_page_name, article_page_text=article_page_text, article_page_number=i)


    return articles_page(request, 'my', 1)

def article(request,article_id):
    user = openaccount(request)
    article = Article.objects.get(id=article_id)
    template = loader.get_template('physicsesc/thisarticle.html')
    context = {
        'article': article,
    }
    return HttpResponse(template.render(context, request))
def article_view(request, article_id):
    user = openaccount(request)
    article = Article.objects.get(id=article_id)
    article_pages = article.article_page_set.all()
    template = loader.get_template('physicsesc/thisarticleview.html')
    context = {
        'article': article,
        'article_pages': article_pages,
    }
    return HttpResponse(template.render(context,request))
def article_vote(request, article_id, vote_type):
    if True:
        user = openaccount(request)
        article = Article.objects.get(id=article_id)
        if vote_type == "vote_for":
            vote_type = True
        elif vote_type == "vote_against":
            vote_type = False
        else:
            return HttpResponse("?????? ???????????? ???????????????? ????????????")
        if len(article.article_vote_set.filter(guest=user)) <= 0:
            if vote_type==True:
                article.article_vote_count = article.article_vote_count + 1
                article.save()
            elif vote_type == False:
                article.article_vote_against_count = article.article_vote_against_count + 1
                article.save()
            article_vote = Article_vote(article=article, vote_type=vote_type, guest=user)
            article_vote.save()
            return render(request, 'physicsesc/thisarticle.html', {'article': article})
        else:
            if article.article_vote_set.get(guest=user).vote_type == vote_type:
                return render(request, 'physicsesc/thisarticle.html', {'article': article, 'alert': '???? ?????? ?????????????????? ?????????? ????????????'})
            else:
                if vote_type == True:
                    article.article_vote_against_count = article.article_vote_against_count - 1
                    article.article_vote_count = article.article_vote_count + 1
                    article.save()
                elif vote_type == False:
                    article.article_vote_count = article.article_vote_count - 1
                    article.article_vote_against_count = article.article_vote_against_count + 1
                    article.save()

            vote = article.article_vote_set.get(guest=user)
            vote.vote_type = vote_type
            vote.save()
            return render(request, 'physicsesc/thisarticle.html', {'article': article})



    return render(request, 'physicsesc/thisarticle.html', {'article': article})

def opengroup(user, group_id):
    group = Group.objects.get(id=group_id)
    can_open = 'no'

    if group.author == user:
        can_open = 'author'
    elif len(group.group_author_helper_set.filter(author_helper=user)) > 0:
        if group.group_author_helper_set.filter(author_helper=user).application_type == True:
            can_open = 'helper'
        else:
            can_open = 'application'
    elif len(group.group_student_set.filter(student=user)) > 0:
        if group.group_student_set.get(student=user).application_type == True:
            can_open = 'student'
        else:
            can_open = 'application'
    return can_open


def openaccount(request):
    try:
        user_name = su_cut(request.COOKIES['user_name'], 40)
        session_key = su_cut(request.COOKIES['session_key'], 100)
        user = Guest.objects.get(guest_name=user_name)
        if len(Guest_session.objects.filter(session_key=session_key, guest_id=user)) == 0:
            return HttpResponse('session inactive | user not found <br> ???????????? ??????????????????|???????????????????????? ???? ????????????')
    except:
        user_name = 'undefined guest'
        user = Guest.objects.get(guest_name=user_name)
    return user
def antiddos(request):
    print(request.META.HTTP_COOKIE)

