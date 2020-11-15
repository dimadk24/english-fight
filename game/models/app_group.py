from django.contrib.auth.models import Group


class AppGroup(Group):
    class Meta:
        verbose_name = 'группа'
        verbose_name_plural = 'группы'
