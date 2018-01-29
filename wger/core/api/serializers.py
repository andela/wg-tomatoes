# -*- coding: utf-8 -*-

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
# along with Workout Manager.  If not, see <http://www.gnu.org/licenses/>.

from rest_framework import serializers
from django.contrib.auth.models import User

from wger.core.models import (Userapi, UserProfile, Language, DaysOfWeek, License,
                              RepetitionUnit, WeightUnit)



class UserapiSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()

        userprofile = user.userprofile
        userprofile.created_by_api = True
        userprofile.save()
        
        my_user = Userapi()
        my_user.user = user
        my_user.created_by_api = self.context["request"].user
        my_user.save()

        return user


    
    
    
    
    
    # Pre-set some values of the user's profile
        language = Language.objects.get(
            short_name=translation.get_language())
        user.userprofile.notification_language = language

        # Set default gym, if needed
        gym_config = GymConfig.objects.get(pk=1)
        if gym_config.default_gym:
            user.userprofile.gym = gym_config.default_gym

            # Create gym user configuration object
            config = GymUserConfig()
            config.gym = gym_config.default_gym
            config.user = user
            config.save()

        user.userprofile.save()
                                 


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('password', 'first_name', 'last_name', 'email',)
        write_only_fields = ('password',)
        read_only_fields = ('is_staff', 'is_active', 'date_joined',)
 
    def restore_object(self, attrs, instance=None):
        user = super(UserSerializer, self).restore_object(attrs, instance)
        user.set_password(attrs['password'])
        return user




class UserprofileSerializer(serializers.ModelSerializer):
    '''
    Workout session serializer
    '''

    class Meta:
        model = UserProfile


class UsernameSerializer(serializers.Serializer):
    '''
    Serializer to extract the username
    '''
    username = serializers.CharField()


class LanguageSerializer(serializers.ModelSerializer):
    '''
    Language serializer
    '''

    class Meta:
        model = Language


class DaysOfWeekSerializer(serializers.ModelSerializer):
    '''
    DaysOfWeek serializer
    '''

    class Meta:
        model = DaysOfWeek


class LicenseSerializer(serializers.ModelSerializer):
    '''
    License serializer
    '''

    class Meta:
        model = License


class RepetitionUnitSerializer(serializers.ModelSerializer):
    '''
    Repetition unit serializer
    '''

    class Meta:
        model = RepetitionUnit


class WeightUnitSerializer(serializers.ModelSerializer):
    '''
    Weight unit serializer
    '''

    class Meta:
        model = WeightUnit
