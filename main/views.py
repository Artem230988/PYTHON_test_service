from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView
from .models import *
from .permissions import *


def index(request):
    return render(request, template_name='test/index.html')


class TestListView(LoginRequiredMixin, ListView):
    model = Test
    template_name = 'test/test_list.html'
    context_object_name = 'tests'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            completed_list = []
            completed_statistics = Statistics.objects.filter(user=self.request.user)
            for c in completed_statistics:
                completed_list.append(c.test.pk)
            queryset = Test.objects.exclude(pk__in=completed_list)

        else:
            queryset = Test.objects.all()

        return queryset


class TestCompleteListView(LoginRequiredMixin, ListView):
    model = Test
    template_name = 'test/completed_test_list.html'
    context_object_name = 'tests'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            completed_list = []
            completed_statistics = Statistics.objects.filter(user=self.request.user)
            for c in completed_statistics:
                completed_list.append(c.test.pk)
            queryset = Test.objects.filter(pk__in=completed_list)
        else:
            queryset = None

        return queryset


@login_required
def create_statistics(request, pk):
    test = get_object_or_404(Test, pk=pk)
    try:
        statistics = Statistics.objects.get(test=test, user=request.user)
        return HttpResponseRedirect(reverse('get_statistics', kwargs={'pk': pk}))
    except:
        if request.method == 'POST':
            k = 0
            for question in test.questions.all():
                if str(question.pk) in request.POST:
                    if str(question.options.get(correct_answer=True).pk) == str(request.POST[str(question.pk)]):
                        k = k + 1
                        Answer.objects.create(test=test, question=question,
                                              option=Options.objects.get(pk=request.POST[str(question.pk)]), correct=True,
                                              user=request.user)
                    else:
                        Answer.objects.create(test=test, question=question,
                                              option=Options.objects.get(pk=request.POST[str(question.pk)]), correct=False,
                                              user=request.user)
                else:
                    Answer.objects.create(test=test, question=question,
                                          option=None, correct=False,
                                          user=request.user)
            Statistics.objects.create(test=test, user=request.user, correct_ans=k)

            return HttpResponseRedirect(reverse('get_statistics', kwargs={'pk': pk}))
        else:
            context = {
                'test': test,
            }
            return render(request, template_name='test/test_detail.html', context=context)


@login_required
def get_statistics(request, pk):
    try:
        test = Test.objects.get(pk=pk)
        statistics = Statistics.objects.get(test=test, user=request.user)
        answers = Answer.objects.filter(test=test)
        count = Answer.objects.filter(test=test).count()
        context = {
            'correct_count': statistics.correct_ans,
            'correct_percent': 100 * statistics.correct_ans / count,
            'answers': answers,
        }
        return render(request, template_name='test/statistics.html', context=context)
    except:
        return render(request, template_name='test/404.html')
