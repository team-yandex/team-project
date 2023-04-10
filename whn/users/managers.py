from django.contrib.auth import models


class UserManager(models.UserManager):
    def users_queryset(self):
        from .models import User

        return (
            self.get_queryset()
            .filter(is_active=True)
            .only(
                User.username.field.name,
                User.email.field.name,
                User.first_name.field.name,
                User.last_name.field.name,
                User.image.field.name,
                User.score.field.name,
            )
        )
