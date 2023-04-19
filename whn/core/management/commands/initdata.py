from glob import glob
from os import environ

from django.core.exceptions import ImproperlyConfigured
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import connections
from django.db import DEFAULT_DB_ALIAS
from django.db.migrations.executor import MigrationExecutor


class Command(BaseCommand):
    help = 'Populate database with initial data'
    requires_migrations_checks = False

    def handle(self, *args, **kwargs):
        """Populate database with initial data"""
        is_migrations_applied = self.apply_migrations()
        if not is_migrations_applied:
            return
        fixture_paths = glob('*/fixtures/*.json')
        call_command('loaddata', fixture_paths)
        superuser_env_variables = [
            'DJANGO_SUPERUSER_USERNAME',
            'DJANGO_SUPERUSER_EMAIL',
            'DJANGO_SUPERUSER_PASSWORD',
        ]
        is_superuser_prompt_interactive = not all(
            environ.get(var) for var in superuser_env_variables
        )
        call_command(
            'createsuperuser',
            interactive=is_superuser_prompt_interactive,
        )

    def apply_migrations(self):
        """
        Print a warning if the set of migrations on disk don't match the
        migrations in the database and automatically apply migrations
        if user wants.
        """
        try:
            executor = MigrationExecutor(connections[DEFAULT_DB_ALIAS])
        except ImproperlyConfigured:
            return False

        plan = executor.migration_plan(executor.loader.graph.leaf_nodes())
        if plan:
            apps_waiting_migration = sorted(
                {migration.app_label for migration, _ in plan}
            )
            self.stdout.write(
                self.style.WARNING(
                    '\nYou have %(unapplied_migration_count)s unapplied '
                    'migration(s). Your project may not work properly '
                    'until you apply the migrations for app(s): '
                    '%(apps_waiting_migration)s.'
                    % {
                        'unapplied_migration_count': len(plan),
                        'apps_waiting_migration': ', '.join(
                            apps_waiting_migration
                        ),
                    }
                )
            )
            answer = ''
            while not answer or answer not in 'yn':
                answer = input('Apply migrations? [yN] ')
                if not answer:
                    answer = 'n'
                    break
                else:
                    answer = answer[0].lower()
            if answer != 'y':
                return False
            call_command('migrate')
        return True
