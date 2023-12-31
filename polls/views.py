from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Choice, Question, Vote


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return all published questions.
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')


class DetailView(generic.DetailView):
    template_name = 'polls/detail.html'
    model = Question

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

    def get(self, request, *args, **kwargs):
        """
        Handles the HTTP GET request for the poll detail page.
        It will be redirected to the poll index page only if
        the poll question does not exist or voting is not allowed.
        """
        try:
            question = get_object_or_404(Question, pk=kwargs['pk'])
        except (Question.DoesNotExist, Http404):
            messages.error(request, f"Poll question {kwargs['pk']}"
                                    f" does not exist.")
            return redirect("polls:index")

        this_user = request.user
        try:
            prev_vote = Vote.objects.get(user=this_user,
                                         choice__question=question)
        except (Vote.DoesNotExist, TypeError):
            prev_vote = None

        if not question.can_vote():
            messages.error(request, f"Poll question {kwargs['pk']}"
                                    f" does not allow voting.")
            return redirect("polls:index")
        else:
            return render(request, self.template_name,
                          {"question": question,
                           "prev_vote": prev_vote})


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

    def get(self, request, *args, **kwargs):
        """
        Handles the HTTP GET request for the poll result page.
        It will be redirected to the poll index page only if
        the poll question does not exist or has not been opened yet.
        """
        try:
            question = get_object_or_404(Question, pk=kwargs['pk'])
        except (Question.DoesNotExist, Http404):
            messages.error(request, f"Poll question {kwargs['pk']}"
                                    f" does not exist.")
            return redirect("polls:index")

        if not question.can_vote():
            messages.error(request, f"Poll question {kwargs['pk']}"
                                    f" has not been opened yet.")
            return redirect("polls:index")
        else:
            return render(request, self.template_name,
                          {"question": question})


@login_required
def vote(request, question_id):
    """
    Handles user voting for a specific poll question.
    """
    question = get_object_or_404(Question, pk=question_id)

    if not question.can_vote():
        messages.error(request, f"Poll question {question_id}"
                                f" does not allow voting.")
        return redirect("polls:index")

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        messages.error(request, "Please select choice")
        return redirect("polls:detail", pk=question_id)

    this_user = request.user
    try:
        # find a vote for this user and this question.
        vote = Vote.objects.get(user=this_user, choice__question=question)
        # update this vote
        vote.choice = selected_choice
    except Vote.DoesNotExist:
        # no matching vote - create a new Vote
        vote = Vote(user=this_user, choice=selected_choice)

    vote.save()
    messages.success(request, f"Your choice ( {vote.choice} ) has been saved.")

    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
