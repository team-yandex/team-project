import django.db.models


class QuestionManager(django.db.models.Manager):
    def published(self):
        return (
            self.get_queryset()
            .filter(is_published=True)
            .prefetch_related('choices')
        )
