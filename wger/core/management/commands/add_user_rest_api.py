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
from wger.core.models import UserProfile, Userapi
from wger.gym.helpers import get_user_last_activity

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    '''
    Handle granting or revoking of permissions to users to add other users via REST API
    '''
    help = 'grant or revoke a user from adding other users via REST API'

    def add_arguments(self, parser):
        '''
        Add required arguments
        '''
        group = parser.add_mutually_exclusive_group()
        group.add_argument(
            '-g',
            '--grantaccesss',
            action='store_true',
            dest='grant',
            help='Grant user permission to add users via REST API',
        )
        group.add_argument(
            '-r',
            '--revokeaccess',
            action='store_true',
            dest='revoke',
            help='Revoke user from adding users via REST API',
        )
        parser.add_argument('username', nargs='?', type=str)

    def handle(self, *args, **options):
        '''
        main method top execute command
        '''
        username = options['username']
        grant = options['grant']
        revoke = options['revoke']

        try:
            user = User.objects.get(username=username)

        except User.DoesNotExist:
            raise CommandError('user with "%s" username does not exist' % username)

        if grant:
            # grant user permission.
            if getattr(user.userprofile, 'can_create_via_api'):
                self.stdout.write(
                    self.style.SUCCESS(
                        '"%s" already has been granted privileges to add users via REST API!!')
                    % username)

            else:
                setattr(user.userprofile, 'can_create_users', True)
                user.userprofile.save()
                self.stdout.write(
                    self.style.SUCCESS(
                        '"%s" has been granted privileges to add users via REST API!!') % username)


        elif revoke:  # revoke permission.
            if not getattr(user.userprofile, 'can_create_users'):
                self.stdout.write(
                    self.style.SUCCESS(
                        '"%s" has no privilege to add users via REST API!!')
                    % username)

            else:
                setattr(user.userprofile, 'can_create_users', False)
                user.userprofile.save()
                self.stdout.write(
                    self.style.SUCCESS(
                        '"%s" has been revoked from add users via REST API!!') % username)

        else:  #  print out a warning since no extra argument was provided.
            self.stdout.write(
                self.style.WARNING(
                    'You need to provide an argument, either "--grant" or "--revoke"'))



        # my_users = User.objects.all()
        # for i in my_users:
        #     self.stdout.write(i.username)
            
                
        

       
        

        

        
