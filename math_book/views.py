from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from .models import Subject, University, Ticket, Guest, Session_tickets, Guest_session, Like, Dislike, Theorem, Vote_theorem, Definition, Vote_definition
from django.template import loader
from django.db.models import Q
from django.urls import reverse
import random
# Create your views here.
