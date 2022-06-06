from django.urls import path

from . import views
app_name= "anonimnetwork"
urlpatterns = [
path('', views.main, name='main'),
#path('spamroom/<int:room_count>', views.spamroom, name='spamroom'),
path('main/', views.main, name='main'),
path('main/page/<int:page_number>/', views.main_page, name='main_page'),
path('new/', views.newrooms, name='newrooms'),
path('newrooms/', views.newrooms, name='newrooms'),
path('new/page/<int:page_number>/', views.newrooms_page, name='newrooms'),
path('newrooms/page/<int:page_number>/', views.newrooms_page, name='newrooms'),
path('top/', views.toprooms, name='toprooms'),
path('top/page/<int:page_number>/', views.toprooms_page, name='toprooms'),
path('toprooms/', views.toprooms, name='toprooms'),
path('toprooms/page/<int:page_number>/', views.toprooms_page, name='toprooms'),
path('channels/', views.channels, name='channels'),
path('channels/page/<int:page_number>/', views.channels_page, name='channels_page'),
path('theme/', views.theme, name='theme'),
path('theme/page/<int:page_number>/', views.theme_page, name='theme_page'),
path('theme/<str:theme_name>', views.themeget, name='themeget'),
path('theme/<str:theme_name>/page/<int:page_number>/', views.themeget_page, name='themeget_page'),
path('createroom/', views.createroom, name='createroom'),
path('sendroom/', views.sendroom, name='sendroom'),
path('findroom/', views.findroom, name='findroom'),
path('getroom/', views.getroom, name='getroom'),
path('openroom/', views.getroom, name='getroom'),
path('<str:room_name>/', views.room, name='room'),
path('<str:room_name>/pinned', views.pinnedmessages, name='pinnedmessages'),
path('<str:room_name>/admin/', views.roomadmin, name='roomadmin'),
path('<str:room_name>/admin/<int:message_id>/', views.messageadmin, name='messageadmin'),
path('<str:room_name>/description', views.description, name='description'),
path('<str:room_name>/page/<int:page_number>', views.roompage, name='roompage'),
path('<str:room_name>/pass', views.roompass, name='roompass'),
path('<str:room_name>/<int:message_id>/', views.message, name='message'),
path('<str:room_name>/<int:message_id>/pin', views.pinmessage, name='pinmessage'),
path('<str:room_name>/<int:message_id>/unpin', views.unpinmessage, name='unpinmessage'),
path('<str:room_name>/<int:message_id>/answer/', views.answer, name='answer'),
path('<str:room_name>/sendmessage/', views.sendmessage, name='sendmessage'),
#path('sendmessage/', views.sendmessage, name='sendmessage'),

#path('useful', views.useful, name='useful'),
#path('sendusefulfile',views.sendusefulfile,name="sendusefulfile"),


]