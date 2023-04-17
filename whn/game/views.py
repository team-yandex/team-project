import datetime
import random

import django.conf
import django.shortcuts
import django.urls
import django.utils
import django.views.generic

import game.forms
import game.models


class QuestionView(django.views.generic.UpdateView):
    template_name = 'game/question.html'
    form_class = game.forms.QuestionForm
    queryset = game.models.Question.objects.published()
    context_object_name = 'question'
    success_url = django.urls.reverse_lazy('game:result')

    def get(self, request, pk, *args, **kwargs):
        if self.request.user.is_authenticated is True:
            question = self.request.user.seen_questions.filter(pk=pk).first()
            if question is None or self.request.session['owner']:
                selected = game.models.Question.objects.get(pk=pk)
                self.request.user.seen_questions.add(selected)
                return super().get(request, *args, **kwargs)
        # to avoid tries to re-run question
        return django.shortcuts.redirect('game:single')

    def form_valid(self, form):
        start_datetime = datetime.datetime.fromisoformat(
            self.request.session['start_datetime']
        )
        end_datetime = start_datetime + datetime.timedelta(
            seconds=self.object.climax_second
            + django.conf.settings.ANSWER_BUFFER_SECONDS
        )
        video = self.object.video
        if (
            form.cleaned_data['choices'].is_correct
            and django.utils.timezone.now() < end_datetime
        ):
            return django.shortcuts.render(
                self.request,
                'game/result.html',
                context={'result': 'ok', 'video': video},
            )
        return django.shortcuts.render(
            self.request,
            'game/result.html',
            context={'result': 'not ok', 'video': video},
        )


class ResultView(django.views.generic.TemplateView):
    template_name = 'game/result.html'


class SingleView(django.views.generic.TemplateView):
    template_name = 'game/single.html'

    def post(self, request, *args, **kwargs):
        # it gets difference between seen and all and chooses random one
        if self.request.user.is_authenticated is True:
            question = random.choice(
                list(
                    game.models.Question.objects.difference(
                        self.request.user.seen_questions.all()
                    )
                )
            )
        # TODO: avoid situation where questions are ended up
        return django.shortcuts.redirect(
            django.urls.reverse('game:question', kwargs=dict(pk=question.id))
        )
