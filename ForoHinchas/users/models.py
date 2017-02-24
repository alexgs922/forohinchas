# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

ALAVES = 'AL'
ATHLETIC_BILBAO = 'AB'
ATLETICO_MADRID = 'AM'
BARCELONA = 'BR'
BETIS = 'BE'
CELTA = 'CE'
DEPORTIVO_CORUNYA = 'DC'
EIBAR = 'EI'
ESPANYOL = 'ES'
GRANADA = 'GR'
LAS_PALMAS = 'LP'
LEGANES = 'LE'
MALAGA = 'MA'
OSASUNA = 'OS'
REAL_MADRID = 'RM'
REAL_SOCIEDAD = 'RS'
SEVILLA = 'SE'
SPORTING = 'SP'
VALENCIA = 'VA'
VILLAREAL = 'VI'

TEAMS = (  # Diccionaro para los equipos
    (ALAVES, 'Alavés'),
    (ATHLETIC_BILBAO, 'Athletic'),
    (ATLETICO_MADRID, 'Atlético'),
    (BARCELONA, 'Barcelona'),
    (BETIS, 'Betis'),
    (CELTA, 'Celta'),
    (DEPORTIVO_CORUNYA, 'Deportivo'),
    (EIBAR, 'Eibar'),
    (ESPANYOL, 'Espanyol'),
    (GRANADA, 'Granada'),
    (LAS_PALMAS, 'Las Palmas'),
    (LEGANES, 'Leganés'),
    (MALAGA, 'Málaga'),
    (OSASUNA, 'Osasuna'),
    (REAL_MADRID, 'R. Madrid'),
    (REAL_SOCIEDAD, 'R. Sociedad'),
    (SEVILLA, 'Sevilla'),
    (SPORTING, 'Sporting'),
    (VALENCIA, 'Valencia'),
    (VILLAREAL, 'Villareal')
)

default = "http://s3.amazonaws.com/37assets/svn/765-default-avatar.png"


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    team = models.CharField(max_length=2, choices=TEAMS)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.URLField(default=default)

    def __unicode__(self):
        return self.user.username


# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()

# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#
# post_save.connect(create_user_profile, sender=User)

# def create_profile(sender, **kwargs):
#     user = kwargs['instance']
#     if kwargs['created']:
#         user_profile = Profile(user=user)
#         user_profile.save()
# post_save.connect(create_profile, sender=User)