import django.urls
import django.views.generic

import game.forms
import game.models


class QuestionView(django.views.generic.UpdateView):
    template_name = 'game/question.html'
    form_class = game.forms.QuestionForm
    queryset = game.models.Question.objects.published()
    context_object_name = 'question'
    success_url = django.urls.reverse_lazy('game:result')

    def form_valid(self, form):
        return django.views.generic.FormView.form_valid(self, form)


class ResultView(django.views.generic.TemplateView):
    template_name = 'game/result.html'
