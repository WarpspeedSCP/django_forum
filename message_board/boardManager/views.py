from django.shortcuts import render

import django

from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

from .models import Forum, Thread, Comment, Attachment, Tag

from .forms import CommentForm, ThreadForm, ForumForm, VoteForm

# Create your views here.

from django.db import connection 


def process_response(request):
    from sys import stdout
    if stdout.isatty():
        for query in connection.queries:
            print ("\033[1;31m[%s]\033[0m \033[1m%s\033[0m" % (query['time'], " ".join(query['sql'].split())))

def index(request):
    process_response(request)
    forums = Forum.objects.order_by('name')
    context = {
        'Forums': forums
    }
    if request.method == 'POST':
        form = ForumForm(request.POST)


        if form.is_valid() and request.user.is_authenticated:
            forum = Forum(name=form.cleaned_data['name'])
            print(form.cleaned_data)
            forum.save()
            return HttpResponseRedirect('')
        else:
            return HttpResponseRedirect('/login')

    elif request.method == 'GET':
        form = ForumForm()

    context['form'] = form

    return render(request, 'index.html', context)


def forum(request, forum_name):
    threads = Thread.objects.filter(
        forum__exact=forum_name).order_by('create_date_time')

    context = {
        'Threads': threads,
        'Forum': forum_name
    }

    if request.method == 'POST':
        print(type(request.user))

        form2 = ThreadForm(request.POST)

        if form2.is_valid():
            if request.user.is_authenticated:
                thr = Thread(name=form2.cleaned_data['name'], forum=Forum.objects.get(
                    name=forum_name), creator=request.user)
                print(thr)
                print(form2.cleaned_data)
                thr.save()
                if all(len(i) > 0 for i in form2.cleaned_data['tags'].split(',')):
                    for tag in form2.cleaned_data['tags'].split(','):
                        thr_tag, created = Tag.objects.get_or_create(tag_name=tag)
                        if created:
                            thr_tag.save()
                        thr.tag_set.add(thr_tag)
                return HttpResponseRedirect('')
            else:
                return HttpResponseRedirect('/login')

    elif request.method == 'GET':
        form2 = ThreadForm()

    context['newThreadForm'] = form2

    return render(request, 'forum.html', context)


def thread(request, forum_name, thread_id):
    comments = Comment.objects.filter(
        thread__exact=thread_id).order_by('create_date_time')

    t = Thread.objects.get(pk=thread_id)

    context = {
        'Comments': comments,
        'Thread': t.name,
        'Tags': t.tag_set.all(),
    }

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CommentForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            if request.user.is_authenticated:
                comm = Comment(
                    contents=form.cleaned_data['comment'], creator=request.user, thread=t)
                comm.save()
                print(request.FILES)
                # myfile is the name of your html file button
                for f in request.FILES.getlist('attachments'):
                    x = Attachment(comment=comm, file=f)
                    x.save()
                return HttpResponseRedirect('')
            else:
                return HttpResponseRedirect('/login')

    elif request.method == 'GET':
        form = CommentForm()
    context['form'] = form
    return render(request, 'thread.html', context)


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect('/login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})
