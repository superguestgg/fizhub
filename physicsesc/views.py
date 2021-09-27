from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from .models import Task, Solution, Guest
from django.template import loader
from django.urls import reverse
def index(request):
    return HttpResponse('<a href="main">main</a>')
def main(request):
    latest_tasks_list = Task.objects.all()
    template = loader.get_template('physicsesc/fizhub.html')
    context = {
        'latest_tasks_list': latest_tasks_list,
    }
    return HttpResponse((template.render(context, request)))
def new(request):
    latest_tasks_list = Task.objects.order_by('-pub_date')[:10]
    template = loader.get_template('physicsesc/fizhub.html')
    context = {
        'latest_tasks_list': latest_tasks_list,
    }
    return HttpResponse(template.render(context, request))
def theme(request):
    return render(request, 'physicsesc/theme.html')
def themefind(request,theme_name1):
    latest_tasks_list = Task.objects.filter(theme1_name=theme_name1)
    template = loader.get_template('physicsesc/fizhub.html')
    context = {
        'latest_tasks_list': latest_tasks_list,
    }
    return HttpResponse(template.render(context, request))
def themefind2(request,theme_name1,theme_name2):
    latest_tasks_list = Task.objects.filter(theme1_name=theme_name1, theme2_name=theme_name2)
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
        template = loader.get_template('physicsesc/fizhub.html')
        context = {
            'latest_tasks_list': latest_tasks_list,
        }
        return HttpResponse(template.render(context, request))
    except:
        return HttpResponse('Server error')
def login(request):
    return render(request, 'physicsesc/login.html')
def sendaccount(request, guest_name):
    #try:
    g=0
    #for guest in (len(Guest.objects.filter(guest_name=guest_name))):
    #    g+=1
    if (len(Guest.objects.filter(guest_name=guest_name)))==0:
        new_user=Guest(guest_name=guest_name)
        new_user.save()
        return HttpResponse('you user_id is '+str(new_user.id))
    return HttpResponse('name reserved|имя занято')
    #except:
        #raise Http404("Error")
def detail(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")
    return render(request, 'physicsesc/thistask.html', {'task': task})
def like(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")
    return render(request, 'physicsesc/thistask.html', {'task': task})
def solution(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
        #solution = Solution.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")
    return render(request, 'physicsesc/thissolution.html', {'task': task})

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

    return HttpResponse('<a href="physic-in-sesc/main>back</a>')
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
def sendtask(request, task_text,theme1_name, theme2_name, creator_name):
    user = Guest.objects.get(id=creator_name)
    #task = Task(task_text=task_text, pub_date=timezone.now(), theme1_name=theme1_name, theme2_name=theme2_name, creator_name=creator_name)
    user.task_set.create(task_text=task_text, pub_date=timezone.now(), theme1_name=theme1_name, theme2_name=theme2_name)
    #print(task.solution_set.solution_text)
    
    return HttpResponse('<a href="physic-in-sesc/main>back</a>')