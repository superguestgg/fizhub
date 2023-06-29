from django.urls import path, re_path

from . import views

app_name = "anonimnetwork"
urlpatterns = [
    path('', views.main, name='main'),
    # path('spamroom/<int:room_count>', views.spam_room, name='spam_room'),

    re_path(r"^(?P<sort_type>main|new|top|channels|newrooms|toprooms)/"
            r"(page/(?P<page_number>[0-9]+)/)?", views.list_rooms, name="list_rooms"),

    path('theme/', views.theme, name='theme'),
    path('theme/page/<int:page_number>/', views.theme_page, name='theme_page'),
    path('theme/<str:theme_name>', views.themeget, name='themeget'),
    path('theme/<str:theme_name>/page/<int:page_number>/', views.themeget_page, name='themeget_page'),
    path('createroom/', views.create_room, name='create_room'),
    path('sendroom/', views.send_room, name='send_room'),
    path('findroom/', views.find_room, name='find_room'),
    path('getroom/', views.get_room, name='get_room'),
    path('openroom/', views.get_room, name='get_room'),
    path('<str:room_name>/', views.room, name='room'),
    path('<str:room_name>/pinned', views.pinned_messages, name='pinned_messages'),
    path('<str:room_name>/admin/', views.room_admin, name='room_admin'),
    path('<str:room_name>/admin/<int:message_id>/', views.message_admin, name='message_admin'),
    path('<str:room_name>/description', views.room_description, name='description'),
    path('<str:room_name>/page/<int:page_number>', views.room_page, name='room_page'),
    path('<str:room_name>/pass', views.room_pass, name='room_pass'),
    path('<str:room_name>/<int:message_id>/', views.message, name='message'),
    path('<str:room_name>/<int:message_id>/pin', views.pin_message, name='pin_message'),
    path('<str:room_name>/<int:message_id>/unpin', views.unpin_message, name='unpin_message'),
    path('<str:room_name>/<int:message_id>/answer/', views.answer, name='answer'),
    path('<str:room_name>/sendmessage/', views.send_message, name='send_message'),
    # path('sendmessage/', views.sendmessage, name='sendmessage'),

    # path('useful', views.useful, name='useful'),
    # path('sendusefulfile',views.sendusefulfile,name="sendusefulfile"),

]
