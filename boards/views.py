from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User

from .models import Board, Topic, Post
from .forms import NewTopicForm

def home(request):
    boards = Board.objects.all()
    context = {
        'boards': boards
    }
    return render(request, 'home.html', context)


def board_topics(request, pk):

    board = get_object_or_404(Board, pk=pk)
    context = {
        'board': board
    }

    return render(request, 'boards/topics.html', context)

def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    user = User.objects.first()

    if request.method == 'POST':
        form = NewTopicForm(request.POST)

        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = user
            topic.save()
            
            post = Post.objects.create(
                message = form.cleaned_data.get('message'),
                topic = topic,
                created_by = user
            )

            return redirect('board_topics', pk=board.pk)

    else:
        form = NewTopicForm()

    context = {
        'board': board,
        'form': form
    }

    return render(request, 'boards/new_topic.html', context)