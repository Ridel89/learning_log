from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import Http404
from .models import Topic, Entry
from .forms import TopicForm, EntryForm


# Create your views here.
def index(request):
    return render(request, 'learning_logs/index.html')


@login_required
def topics(request):
    user_topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'user_topics': user_topics}
    return render(request, 'learning_logs/topics.html', context)


def check_topic_owner(selected_topic, request):
    if selected_topic.owner != request.user:
        raise Http404


@login_required
def topic(request, topic_id):
    selected_topic = Topic.objects.get(id=topic_id)
    check_topic_owner(selected_topic, request)

    entries = selected_topic.entry_set.order_by('-date_added')
    context = {'selected_topic': selected_topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)


@login_required
def new_topic(request):
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic1 = form.save(commit=False)
            new_topic1.owner = request.user
            new_topic1.save()
            return redirect('learning_logs:topics')

    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    topic1 = Topic.objects.get(id=topic_id)
    check_topic_owner(topic1, request)

    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry1 = form.save(commit=False)
            new_entry1.topic = topic1
            new_entry1.save()
            return redirect('learning_logs:topic', topic_id=topic_id)

    context = {'form': form, 'topic': topic1}
    return render(request, 'learning_logs/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    entry1 = Entry.objects.get(id=entry_id)
    topic1 = entry1.topic
    check_topic_owner(topic1, request)

    if request.method != 'POST':
        form = EntryForm(instance=entry1)
    else:
        form = EntryForm(instance=entry1, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic1.id)

    context = {'form': form, 'topic': topic1, 'entry': entry1}
    return render(request, 'learning_logs/edit_entry.html', context)


