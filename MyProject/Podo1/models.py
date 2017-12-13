# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

class EmpProfile(models.Model):
    """To keep extra user data"""
    # user mapping
    user = models.OneToOneField(User)
    class Meta(object):
        verbose_name = _(u"Профіль користувача")

    # extra user data
    level = models.CharField (
        max_length=12,
        blank=True,
        verbose_name=_ (u"Level"),
        default='')

    mobile_phone = models.CharField(
        max_length=12,
        blank=True,
        verbose_name=_(u"Мобільний телефон"),
        default='')

    def __unicode__(self):
        return self.user.username