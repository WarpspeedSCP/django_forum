from django.shortcuts import render

import django

from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect

from .models import Forum, Thread, Comment, Attachment, Tag

from .forms import CommentForm, ThreadForm, ForumForm, VoteForm

# Create your views here.


def index(request):
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


def userconf(request):
    return HttpResponse('BBS User Config Page!')
