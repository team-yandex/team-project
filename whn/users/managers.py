from django.contrib.auth import models

import users.models


class UserManager(models.UserManager):
    def users_queryset(self):
        return (
            self.get_queryset()
            .filter(is_active=True)
            .only(
                users.models.User.username.field.name,
                users.models.User.email.field.name,
                users.models.User.first_name.field.name,
                users.models.User.last_name.field.name,
                users.models.User.image.field.name,
                users.models.User.score.field.name,
            )
        )
