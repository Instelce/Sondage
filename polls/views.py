from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Choice, Question


class IndexView(generic.ListView):
    model = Question
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
            Return the last five published questions (not including those set to be
            published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    extra_context = {'title': 'Voter'}

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class QuestionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Question
    fields = ['question_text', 'pub_date']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ChoiceCreateView(LoginRequiredMixin, generic.CreateView):
    model = Choice
    fields = ['choice_text', 'question']
    success_url = '/'

    def form_valid(self, form):
        return super().form_valid(form)


class QuestionUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Question
    fields = ['question_text', 'pub_date']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        question = self.get_object()
        if self.request.user == question.author:
            return True
        return False


class QuestionDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Question
    success_url = '/'

    def test_func(self):
        question = self.get_object()
        if self.request.user == question.author:
            return True
        return False


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
    extra_context = {'title': 'Detail'}


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form
        context = {'question': question, 'error_message': "Tu n'as rien choisit !"}
        return render(request, 'polls/detail.html', context)
    else:
        selected_choice.votes += 1
        selected_choice.save()
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
