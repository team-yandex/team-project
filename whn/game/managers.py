import random

import django.db.models


class QuestionManager(django.db.models.Manager):
    def published(self):
        # TODO: only necessary fields
        return (
            self.get_queryset()
            .filter(is_published=True)
            .prefetch_related('choices')
        )

    def random(self):
        max_id = self.published().aggregate(max_id=django.db.models.Max('id'))[
            'max_id'
        ]
        while True:
            pk = random.randint(1, max_id)
            question = self.get_queryset().filter(pk=pk).first()
            if question:
                return question
