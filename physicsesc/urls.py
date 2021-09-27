from django.urls import path

from . import views
app_name= "physicsesc"
urlpatterns = [
path('', views.main, name='index'),
path('main', views.main, name='main'),
path('new', views.new, name='new'),
path('login', views.login, name='login'),
path('theme', views.theme, name='theme'),
path('theme/<str:theme_name1>', views.themefind, name='themefind'),
path('theme/<str:theme_name1>/<str:theme_name2>', views.themefind2, name='themefind2'),
path('user', views.user, name='user'),
path('user/<str:user_name>', views.userfind, name='userfind'),
path('sendaccount/<str:guest_name>', views.sendaccount, name='sendaccount'),
path('<int:task_id>/', views.detail, name='detail'),
path('<int:task_id>/like', views.like, name='like'),
path('<int:task_id>/solution/', views.solution, name='solution'),
path('<int:task_id>/makesolution/', views.makesolution, name='makesolution'),
#path('<int:task_id>/makesolution2/', views.makesolution2, name='makesolution2'),
path('<int:task_id>/makesolution3/<str:solution_text>', views.makesolution3, name='makesolution3'),
path('createtask/', views.createtask, name='createtask'),
path('sendtask/<str:task_text>/<str:creator_name>/<str:theme1_name>/<str:theme2_name>', views.sendtask, name='sendtask'),

]