from django.apps import AppConfig
from django.contrib.auth.management import create_permissions
from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_migrate


class UserConfig(AppConfig):
    name = 'user'

    def ready(self):
        post_migrate.connect(self.create_group, sender=self)

    def create_group(apps, schema_editor):

        for app_config in apps.get_app_configs():
            create_permissions(app_config, apps=apps, verbosity=0)

        group, created = Group.objects.get_or_create(name='consensus_user')
        if created:
            add_thing = Permission.objects.get(codename='add_school')
            group.permissions.add(add_thing)
            group.save()
