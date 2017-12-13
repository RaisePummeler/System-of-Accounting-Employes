# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Employee(models.Model):
    class Meta (object):
        verbose_name = u"Працівник"
        verbose_name_plural = u"Працівники"

    first_name = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=u"Ім'я")

    last_name = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=u"Прізвище")

    middle_name = models.CharField(
        max_length=256,
        blank=True,
        verbose_name=u"По-батькові",
        default='')

    level = models.CharField (
        max_length=256,
        blank=True,
        verbose_name=u"Кваліфікація",
        default=' ')

    employee_group = models.ForeignKey ('Group',
        verbose_name=u"Проект",
        blank=True,
        null=True,
        default=' ',
        on_delete=models.PROTECT)

    birthday = models.DateField(
        verbose_name=u"Дата народження",
        blank=True,
        null=True,
        default = ' ')

    adress = models.CharField (
        max_length=256,
        blank=True,
        verbose_name=u"Адреса проживання",
        default=' ')

    Numb = models.CharField (
        max_length=256,
        blank=True,
        verbose_name=u"Телефон(моб.)",
        default=' ')

    education = models.CharField (
        max_length=256,
        blank=True,
        verbose_name=u"Освіта",
        default=' ')

    exp = models.CharField(
        max_length=256,
        blank=True,
        verbose_name=u"Досвід(роки)",
        default=' ')

    photo = models.ImageField(
        blank=True,
        verbose_name=u"Фото",
        null=True)

    notes = models.TextField(
        blank=True,
        verbose_name=u"Додаткові нотатки")

    def __unicode__(self):
        return u"%s %s" % (self.first_name, self.last_name)

########################################################################################################################
class Group(models.Model):
    class Meta (object):
        verbose_name = u"Проект"
        verbose_name_plural = u"Проекти"

    title = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=u"Назва")

    leader = models.OneToOneField('Employee',
        verbose_name=u"Керівник",
        blank = True,
        null = True,
        on_delete = models.SET_NULL)

    notes = models.TextField(
        blank=True,
        verbose_name=u"Додаткові нотатки")

    def __unicode__(self):
        if self.leader:
            return u" % s ( % s % s)" % (self.title, self.leader.first_name, self.leader.last_name)
        else:
            return u" % s" % (self.title,)

########################################################################################################################
class MonthJournal(models.Model):
    """Student Monthly Journal"""
    class Meta:
        verbose_name = u'Місячний Журнал'
        verbose_name_plural = u'Місячні Журнали'

    employee = models.ForeignKey('Employee', verbose_name=u'Працівник',blank=False, unique_for_month='date')
    # we only need year and month, so always set day to first day of the month
    date = models.DateField(verbose_name=u'Дата', blank=False)

    # list of days, each says whether student was presenе or not
    present_day1 = models.BooleanField(default=False)
    present_day2 = models.BooleanField(default=False)
    present_day3 = models.BooleanField(default=False)
    present_day4 = models.BooleanField(default=False)
    present_day5 = models.BooleanField(default=False)
    present_day6 = models.BooleanField(default=False)
    present_day7 = models.BooleanField(default=False)
    present_day8 = models.BooleanField(default=False)
    present_day9 = models.BooleanField(default=False)
    present_day10 = models.BooleanField(default=False)
    present_day11 = models.BooleanField(default=False)
    present_day12 = models.BooleanField(default=False)
    present_day13 = models.BooleanField(default=False)
    present_day14 = models.BooleanField(default=False)
    present_day15 = models.BooleanField(default=False)
    present_day16 = models.BooleanField(default=False)
    present_day17 = models.BooleanField(default=False)
    present_day18 = models.BooleanField(default=False)
    present_day19 = models.BooleanField(default=False)
    present_day20 = models.BooleanField(default=False)
    present_day21 = models.BooleanField(default=False)
    present_day22 = models.BooleanField(default=False)
    present_day23 = models.BooleanField(default=False)
    present_day24 = models.BooleanField(default=False)
    present_day25 = models.BooleanField(default=False)
    present_day26 = models.BooleanField(default=False)
    present_day27 = models.BooleanField(default=False)
    present_day28 = models.BooleanField(default=False)
    present_day29 = models.BooleanField(default=False)
    present_day30 = models.BooleanField(default=False)
    present_day31 = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s: %d, %d' % (self.employee.last_name, self.date.month, self.date.year)


#########################################################################################################################
