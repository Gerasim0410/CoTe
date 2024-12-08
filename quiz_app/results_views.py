from django.apps import apps
from django.urls import reverse
from django.forms import modelform_factory
from django.http import Http404
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import Questions, Question, TestSession, Profile, \
    Answer, Answers, Results

json_dumps_params = {"ensure_ascii": False}


def available_models(request):
    data_models = \
        [i.__name__
         for i in [Questions, Question, TestSession,
                   Profile, Answer, Answers, Results]]
    return render(request, 'model_list.html', {'models': data_models})


@login_required
def detailed_results_view(request):
    users = Profile.objects.all()

    results_by_user = {}

    for user in users:
        user_results = {}
        answers = Answers.objects.filter(user_id=user).all()
        for answer in answers:
            results = Results.objects.filter(answers_id=answer)
            for result in results:
                test_type = result.questions_id.test_type
                if test_type not in user_results:
                    user_results[test_type] = {}
                if 'answers' not in user_results[test_type]:
                    user_results[test_type]['answers'] = []
                if any([i in test_type
                        for i in ['STROOP', 'ARITHM', 'RAVEN']]):
                    for answer, result in zip(
                            [i for i in Answer.objects.all()
                             if answer.answers_id == i.answers_series_id],
                            [i for i in result.result[1:-1].split(',')]):
                        user_results[test_type]['answers'].append(
                            {'result': result,
                             'answer_num': answer.answer_num,
                             'given_answer': answer.given_answer,
                             'right_answer': answer.right_answer})
                else:
                    answer = [i for i in Answer.objects.all()
                              if answer.answers_id == i.answers_series_id][0]
                    user_results[test_type]['answers'].append(
                        {'result': result.result,
                         'answer_num': answer.answer_num,
                         'given_answer': answer.given_answer,
                         'right_answer': answer.right_answer})

        results_by_user[user.user_id] = user_results

    context = {
        'results_by_user': results_by_user,
    }

    return render(request, 'detailed_results.html', context)


def get_model(model_name):
    try:
        return apps.get_model('quiz_app', model_name)
    except LookupError:
        raise Http404(f'Model {model_name} does not exist')


def model_list(request, model_name):
    model = get_model(model_name)
    view = BaseTableView.as_view(model=model)
    return view(request)


def model_create(request, model_name):
    model = get_model(model_name)
    view = BaseTableCreateUpdateView.as_view(model=model)
    return view(request)


def model_update(request, model_name, pk):
    model = get_model(model_name)
    view = BaseTableCreateUpdateView.as_view(model=model)
    return view(request, pk=pk)


@login_required
def model_delete(request, model_name, pk):
    model = get_model(model_name)
    item = get_object_or_404(model, pk=pk)

    if request.method == 'POST':
        item.delete()
        return redirect(reverse('item_list', args=[model_name]))

    return render(request, 'item_confirm_delete.html',
                  {'item': item,
                   'model': model_name})


class BaseTableView(View):
    model = None
    template_name_list = 'item_list.html'

    def get(self, request):
        items = self.model.objects.all()
        fields = \
            [field.name for field in self.model._meta.get_fields()]
        column_count = len(fields) + 2
        context = {'items': [i if i is not None else 'N/A' for i in items],
                   'fields': fields,
                   'column_count': column_count,
                   'model': self.model.__name__}
        return render(request, self.template_name_list, context)


class BaseTableCreateUpdateView(View):
    model = None
    template_name_form = 'item_form.html'

    @method_decorator(login_required)
    def get(self, request, pk=None):
        form = modelform_factory(self.model, fields='__all__')
        if pk:
            item = get_object_or_404(self.model, pk=pk)
            form = form(instance=item)
        else:
            form = form()
        return render(request, self.template_name_form,
                      {'form': form,
                       'model': self.model.__name__})

    @method_decorator(login_required)
    def post(self, request, pk=None):
        form = modelform_factory(self.model, fields='__all__')
        if pk:
            item = get_object_or_404(self.model, pk=pk)
            form = form(request.POST, instance=item)
        else:
            form = form(request.POST)

        if form.is_valid():
            form.save()
            return redirect(reverse(
                'item_list',
                kwargs={'model_name': self.model.__name__}))
        return render(request, self.template_name_form,
                      {'form': form,
                       'model': self.model.__name__})
