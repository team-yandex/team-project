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
            if question is None:
                selected = game.models.Question.objects.get(pk=pk)
                self.request.user.seen_questions.add(selected)
                return super().get(request, *args, **kwargs)
            else:
                return django.shortcuts.render(
                    request, 'game/do_not_deceive.html'
                )
        # to avoid tries to re-run question
        return django.shortcuts.redirect('info:index_page')

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
            # TODO: Anonymous user should avoid it
            if self.request.user.is_authenticated is True:
                self.request.user.score += self.object.score
                self.request.user.save()
            return django.shortcuts.render(
                self.request,
                'game/result.html',
                context={
                    'result': 'ok',
                    'video': video,
                    'earned': self.object.score,
                },
            )
        return django.shortcuts.render(
            self.request,
            'game/result.html',
            context={'result': 'not ok', 'video': video, 'earned': -1},
        )


class ResultView(django.views.generic.TemplateView):
    template_name = 'game/result.html'


class SingleView(django.views.generic.TemplateView):
    template_name = 'game/single.html'

    def post(self, request, *args, **kwargs):
        # it gets difference between seen and all and chooses random one
        if self.request.user.is_authenticated is True:
            questions = list(
                set(
                    game.models.Question.objects.published().values_list(
                        'id', flat=True
                    )
                ).difference(
                    self.request.user.seen_questions.values_list(
                        'id', flat=True
                    )
                )
            )
            if questions:
                return django.shortcuts.redirect(
                    django.urls.reverse(
                        'game:question',
                        kwargs=dict(pk=random.choice(questions)),
                    )
                )
            else:
                return django.shortcuts.render(
                    self.request, 'game/completed.html'
                )
        else:
            return django.shortcuts.redirect('users:login')
