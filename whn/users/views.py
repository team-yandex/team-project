from datetime import timedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import DetailView, FormView, ListView, TemplateView

from .forms import (
    CustomUserChangeForm,
    CustomUserCreationForm,
)
from .models import User


class SignUpView(FormView):
    template_name = 'users/sign_up.html'
    model = User
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form):
        username = form.cleaned_data[self.model.username.field.name]
        email = form.cleaned_data[self.model.email.field.name]

        user = form.save()
        user.is_active = settings.IS_ACTIVE
        user.save()

        if not settings.IS_ACTIVE:
            mail_text = f"""Здравствуйте!

Вы получили это сообщение, так как зарегистрировались на Yadjango.

Для активации своего профиля перейдите по ссылке:
{self.request.build_absolute_uri(reverse('users:activate',
                                         kwargs={'username': username}))}

Спасибо, что присоединились к нам!

© Yadjango
"""
            send_mail(
                'Yadjango company',
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
            is_active=0,
        )

        is_link_expired = timezone.now() - user.date_joined > timedelta(
            hours=12
        )

        if is_link_expired:
            raise Http404('Link expired')

        user.is_active = 1
        user.save()

        context = super().get_context_data(**kwargs)
        context['username'] = self.kwargs['username']

        return render(request, self.template_name, context)


class UsersList(ListView):
    queryset = (
        User.objects.get_queryset()
        .filter(is_active=True)
        .order_by(User.username.field.name)
        .only(
            User.username.field.name,
            User.first_name.field.name,
            User.last_name.field.name,
            User.image.field.name,
            User.score.field.name,
        )
    )
    template_name = 'users/users_list.html'
    context_object_name = 'users'


class UserDetail(DetailView):
    queryset = (
        User.objects.get_queryset()
        .only(
            User.username.field.name,
            User.email.field.name,
            User.first_name.field.name,
            User.last_name.field.name,
            User.image.field.name,
            User.score.field.name,
        )
        .filter(is_active=1)
    )
    template_name = 'users/user_detail.html'
    context_object_name = 'user_pk'


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(
            User.objects.get_queryset()
            .only(
                User.username.field.name,
                User.email.field.name,
                User.first_name.field.name,
                User.last_name.field.name,
                User.image.field.name,
                User.score.field.name,
            ),
            id=request.user.id,
            is_active=1,
        )

        self.form = CustomUserChangeForm(request.POST or None, instance=user)

        context = {
            'form': self.form,
            'user_me': user,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(
            User.objects.get_queryset()
            .only(
                User.username.field.name,
                User.email.field.name,
                User.first_name.field.name,
                User.last_name.field.name,
                User.image.field.name,
                User.score.field.name,
            ),
            id=request.user.id,
            is_active=1,
        )

        self.form = CustomUserChangeForm(request.POST or None, instance=user)

        if self.form.is_valid():
            self.form.save()

            messages.success(request, 'Изменения сохранены')

            return redirect('users:profile')


class CustomLoginView(LoginView):
    redirect_authenticated_user = True
