# -*- coding: utf-8 -*-
from dateutil.relativedelta import relativedelta
from calendar import monthrange, weekday, day_abbr
from django.core.urlresolvers import reverse
from Prog.models import Employee, MonthJournal
from datetime import datetime, date
from django.views.generic import TemplateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


########################################################################################################################
def paginate(objects, size, request, context, var_name='object_list'):
    """Paginate objects provided by view.
       This function takes:
           * list of elements;
           * number of objects per page;
           * request object to get url parameters from;
           * context to set new variables into;
           * var_name - variable name for list of objects.
       It returns updated context object."""

    # apply pagination
    paginator = Paginator(objects, size)
    # try to get page number from request
    page = request.GET.get ('page', '1')
    try:
        object_list = paginator.page (page)
    except PageNotAnInteger:
        # if page is not an integer, deliver first page
        object_list = paginator.page (1)
    except EmptyPage:
        # if page is out of range (e.g. 9999), deliver last page of results
        object_list = paginator.page (paginator.num_pages)
    # set variables into context
    context[var_name] = object_list
    context['is_paginated'] = object_list.has_other_pages ()
    context['page_obj'] = object_list
    context['paginator'] = paginator
    return context

########################################################################################################################
class JournalView(TemplateView):
    template_name = 'Prog\\journal.html'

    @method_decorator (login_required)
    def dispatch(self, *args, **kwargs):
        return super (JournalView, self).dispatch (*args, **kwargs)

    def get_context_data(self, **kwargs):
        # get context data from TemplateView class
        context = super (JournalView, self).get_context_data (**kwargs)
        
        # check if we need to display some specific month
        if self.request.GET.get ('month'):
            month = datetime.strptime (self.request.GET['month'], '%Y-%m-%d' ).date ()
        else:
            # otherwise just displaying current month data
            today = datetime.today()
            month = date(today.year, today.month, 1)

        # calculate current, previous and next month details;
        # we need this for month navigation element in template
        next_month = month + relativedelta (months=1)
        prev_month = month - relativedelta (months=1)
        context['prev_month'] = prev_month.strftime ('%Y-%m-%d')
        context['next_month'] = next_month.strftime ('%Y-%m-%d')
        context['year'] = month.year
        context['month_verbose'] = month.strftime ('%B')
        # we'll use this variable in employees pagination
        context['cur_month'] = month.strftime ('%Y-%m-%d')
        # prepare variable for template to generate journal table header elements
        myear, mmonth = month.year, month.month
        number_of_days = monthrange (myear, mmonth)[1]
        context['month_header'] = [{'day': d,'verbose': day_abbr[weekday(myear, mmonth, d)][:2]} for d in range (1, number_of_days + 1)]

        # get all employee from database
        if kwargs.get ('pk'):
            queryset = [Employee.objects.get (pk=kwargs['pk'])]

        else:
            queryset = Employee.objects.all ().order_by ('last_name')
        # url to update employee presence, for form post
        update_url = reverse ('journal')

        # пробігаємось по усіх студентах і збираємо необхідні дані:
        employee = []
        for employees in queryset:
            # try to get journal object by month selected
            # month and current employee
            try:
                journal = MonthJournal.objects.get (employee=employees, date=month)
            except Exception:
                journal = None
            # fill in days presence list for current employee
            days = []
            for day in range (1, number_of_days+1):
                days.append ({
                    'day': day,
                    'present': journal and getattr(journal, 'present_day%d' % day, False) or False,
                    'date': date(myear, mmonth, day).strftime('%Y-%m-%d'),})
            # набиваємо усі решту даних студента
            employee.append({
                    'fullname': u'%s %s' % (employees.last_name, employees.first_name),
                    'days': days,
                    'id': employees.id,
                    'update_url': update_url,})
        # застосовуємо піганацію до списку студентів
        context = paginate (employee, 10, self.request, context, var_name ='employee')
        # повертаємо оновлений словник із даними
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST
        # prepare employee, dates and presence data
        current_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        month = date(current_date.year, current_date.month, 1)
        present = data['present'] and True or False
        employee = Employee.objects.get(pk=data['pk'])
        # get or create journal object for given employee and month
        journal = MonthJournal.objects.get_or_create(employee=employee, date=month)[0]
        # set new presence on journal for given employee and save result    
        setattr(journal, 'present_day%d' % current_date.day, present)
        journal.save()
        # return success status
        return JsonResponse({'status': 'success'})
