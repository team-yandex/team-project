import random

import django.db.models

import game.models


class QuestionManager(django.db.models.Manager):
    def published(self):
        # TODO: only necessary fields
        return (
            self.get_queryset()
            .filter(is_published=True)
            .prefetch_related(
                game.models.Choice.question.field.remote_field.name
            )
        )

    def random(self, exclude=None):
        pks = self.published().values_list('pk', flat=True)
        if exclude is not None:
            pks = list(set(pks) - set(exclude))
        if pks:
            random_pk = random.choice(pks)
            return self.get(pk=random_pk)
        return None
