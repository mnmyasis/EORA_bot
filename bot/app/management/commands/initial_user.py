# -*- coding: utf-8 -*-
import os

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import IntegrityError

User = get_user_model()


class Command(BaseCommand):
    help = 'Инициализация суперюзера'

    def handle(self, *args, **options):

        try:
            User.objects.create_superuser(
                username=os.getenv('DJANGO_ADMIN_USERNAME'),
                password=os.getenv('DJANGO_ADMIN_PASSWORD'),
                email=os.getenv('DJANGO_ADMIN_EMAIL', 'admin@gmail.com'),
                first_name=os.getenv('DJANGO_ADMIN_FIRST_NAME', 'admin'),
                last_name=os.getenv('DJANGO_ADMIN_LAST_NAME', 'admin'),
            )
        except IntegrityError:
            print('Пользователь уже создан')