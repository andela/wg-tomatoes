# -*- coding: utf-8 *-*

# This file is part of wger Workout Manager.
#
# wger Workout Manager is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# wger Workout Manager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from wger.gym.helpers import get_user_last_activity
from wger.core.models import Userapi



class Command(BaseCommand):
    '''
    Adds a user to the table
    '''

    help = "List a user"

    def handle(self,*args, **options):
        '''
        Process the options
        '''
        my_users = Userapi.objects.all()
        for i in my_users:
            self.stdout.write(i.user.username)

        
