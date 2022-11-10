from django.urls import path

from . import views

urlpatterns = [
    path('sendpost_subject', views.send_subject, name='send_subject'),
path('subject/', views.get_subject, name='get_subject'),
path('subjects/', views.show_all_subject, name='show_all_subject'),
path('subjects/<str:sort_type>/', views.show_subject, name='show_subject'),
path('subjects/<str:sort_type>/page/<int:page_number>/', views.show_subject_page, name='show_subject_page'),
path('subject/<int:subject_number>/tickets/', views.show_all_ticket_from_subject, name='show_all_ticket'),
path('subject/<int:subject_number>/tickets/<str:sort_type>/', views.show_ticket_from_subject, name='show_ticket'),
path('subject/<int:subject_number>/tickets/<str:sort_type>/page/<int:page_number>/', views.show_ticket_from_subject_page, name='show_ticket_page'),
path('subject/<int:subject_number>/theorems/', views.show_all_theorem_from_subject, name='show_all_theorem'),
path('subject/<int:subject_number>/theorems/<str:sort_type>/', views.show_theorem_from_subject, name='show_theorem'),
path('subject/<int:subject_number>/theorems/<str:sort_type>/page/<int:page_number>/', views.show_theorem_from_subject_page, name='show_theorem_page'),
path('subject/<int:subject_number>/definitions/', views.show_all_definition_from_subject, name='show_all_definition'),
path('subject/<int:subject_number>/definitions/<str:sort_type>/', views.show_definition_from_subject, name='show_definition'),
path('subject/<int:subject_number>/definitions/<str:sort_type>/page/<int:page_number>/', views.show_definition_from_subject_page, name='show_definition_page'),
path('subject/create_subject/', views.create_subject, name='create_subject'),
path('sendpost_university', views.send_university, name='send_university'),
path('university/', views.get_university, name='get_university'),
path('universitys/', views.show_all_university, name='show_all_university'),
path('universitys/<str:sort_type>/', views.show_university, name='show_university'),
path('universitys/<str:sort_type>/page/<int:page_number>/', views.show_university_page, name='show_university_page'),
path('university/<int:university_number>/tickets/', views.show_all_ticket_from_university, name='show_all_ticket'),
path('university/<int:university_number>/tickets/<str:sort_type>/', views.show_ticket_from_university, name='show_ticket'),
path('university/<int:university_number>/tickets/<str:sort_type>/page/<int:page_number>/', views.show_ticket_from_university_page, name='show_ticket_page'),
path('university/<int:university_number>/sessions/', views.show_all_session_from_university, name='show_all_session'),
path('university/<int:university_number>/sessions/<str:sort_type>/', views.show_session_from_university, name='show_session'),
path('university/<int:university_number>/sessions/<str:sort_type>/page/<int:page_number>/', views.show_session_from_university_page, name='show_session_page'),
path('university/create_university/', views.create_university, name='create_university'),
path('sendpost_ticket', views.send_ticket, name='send_ticket'),
path('ticket/', views.get_ticket, name='get_ticket'),
path('tickets/', views.show_all_ticket, name='show_all_ticket'),
path('tickets/<str:sort_type>/', views.show_ticket, name='show_ticket'),
path('tickets/<str:sort_type>/page/<int:page_number>/', views.show_ticket_page, name='show_ticket_page'),
path('ticket/create_ticket/', views.create_ticket, name='create_ticket'),
path('sendpost_vote_ticket', views.send_vote_ticket, name='send_vote_ticket'),
path('sendpost_session', views.send_session, name='send_session'),
path('session/', views.get_session, name='get_session'),
path('sessions/', views.show_all_session, name='show_all_session'),
path('sessions/<str:sort_type>/', views.show_session, name='show_session'),
path('sessions/<str:sort_type>/page/<int:page_number>/', views.show_session_page, name='show_session_page'),
path('session/create_session/', views.create_session, name='create_session'),
path('sendpost_theorem', views.send_theorem, name='send_theorem'),
path('theorem/', views.get_theorem, name='get_theorem'),
path('theorems/', views.show_all_theorem, name='show_all_theorem'),
path('theorems/<str:sort_type>/', views.show_theorem, name='show_theorem'),
path('theorems/<str:sort_type>/page/<int:page_number>/', views.show_theorem_page, name='show_theorem_page'),
path('theorem/create_theorem/', views.create_theorem, name='create_theorem'),
path('sendpost_vote_theorem', views.send_vote_theorem, name='send_vote_theorem'),
path('sendpost_definition', views.send_definition, name='send_definition'),
path('definition/', views.get_definition, name='get_definition'),
path('definitions/', views.show_all_definition, name='show_all_definition'),
path('definitions/<str:sort_type>/', views.show_definition, name='show_definition'),
path('definitions/<str:sort_type>/page/<int:page_number>/', views.show_definition_page, name='show_definition_page'),
path('definition/create_definition/', views.create_definition, name='create_definition'),
path('sendpost_vote_definition', views.send_vote_definition, name='send_vote_definition'),
]