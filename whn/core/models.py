from django.db import models
from django_cleanup.signals import cleanup_pre_delete
from sorl.thumbnail import delete, get_thumbnail


class ImageBaseModel(models.Model):
    image = models.ImageField(
        'Будет приведено к ширине 300px', upload_to='media/%Y/%m/', default=''
    )

    class Meta:
        abstract = True

    @property
    def get_image_300x300(self):
        return get_thumbnail(self.image, '300x300', crop='center', quality=51)

    def sorl_delete(**kwargs):
        delete(kwargs['file'])

    cleanup_pre_delete.connect(sorl_delete)
