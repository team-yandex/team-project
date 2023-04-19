from datetime import timedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.http import HttpResponseGone
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import DetailView
from django.views.generic import FormView
from django.views.generic import ListView
from django.views.generic import TemplateView

from users.forms import UserChangeForm
from users.forms import UserCreationForm
from users.models import User


class SignUpView(FormView):
    template_name = 'users/sign_up.html'
    model = User
    form_class = UserCreationForm
    success_url = reverse_lazy('users:profile')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('users:profile')

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        username = form.cleaned_data[self.model.username.field.name]
        email = form.cleaned_data[self.model.email.field.name]

        subject_template_name = 'users/email_texts/sign_up.html'
        context = {
            'link': self.request.build_absolute_uri(
                reverse('users:activate', kwargs={'username': username})
            )
        }
        mail_text = render_to_string(subject_template_name, context)

        user = form.save()
        user.is_active = settings.IS_ACTIVE
        user.save()

        if not settings.IS_ACTIVE:
            send_mail(
                'Whn',
                mail_text,
                settings.ADMIN_EMAIL,
                [email],
                fail_silently=False,
            )

        return super().form_valid(form)


class Activate(TemplateView):
    model = User
    template_name = 'users/activate.html'

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(
            self.model.objects.get_queryset(),
            username=self.kwargs['username'],
            is_active=False,
        )
        timedelta_ago_joined = user.date_joined - timezone.localtime()
        timedelta_ago_joined -= timedelta(
            microseconds=timedelta_ago_joined.microseconds
        )
        is_link_expired = timedelta_ago_joined > timedelta(hours=12)

        if is_link_expired:
            return HttpResponseGone('Link expired')

        user.is_active = 1
        user.save()

        context = super().get_context_data(**kwargs)
        context['username'] = self.kwargs['username']

        return render(request, self.template_name, context)


class LeaderBoard(ListView):
    queryset = (
        User.objects.users_queryset()
        .only(
            User.username.field.name,
            User.first_name.field.name,
            User.last_name.field.name,
            User.image.field.name,
            User.score.field.name,
        )
        .order_by(f'-{User.score.field.name}')
    )
    template_name = 'users/leaderboard.html'
    context_object_name = 'users'
    paginator_class = Paginator
    paginate_by = settings.PAGINATE_BY


class UserDetail(DetailView):
    queryset = User.objects.users_queryset()

    template_name = 'users/user_detail.html'
    context_object_name = 'user_pk'


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(
            User.objects.users_queryset(),
            id=request.user.id,
        )

        self.form = UserChangeForm(
            request.POST or None, files=request.FILES or None, instance=user
        )

        context = {
            'form': self.form,
            'user_me': user,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(
            User.objects.users_queryset(),
            id=request.user.id,
        )

        self.form = UserChangeForm(
            request.POST or None, files=request.FILES or None, instance=user
        )

        if self.form.is_valid():
            self.form.save()

            messages.success(request, 'Изменения сохранены')

            return redirect('users:profile')


class CustomLoginView(LoginView):
    redirect_authenticated_user = True

    def form_valid(self, form):
        response = super().form_valid(form)
        if 'score' in self.request.session:
            self.request.user.score = self.request.session['score']
        if 'seen_questions' in self.request.session:
            for pk in self.request.session['seen_questions']:
                if not self.request.user.seen_questions.filter(pk=pk).exists():
                    self.request.user.seen_questions.add(pk)
        self.request.user.save()
        return response
