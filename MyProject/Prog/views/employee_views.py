# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.views.generic import ListView
from Prog.models import Employee, Group
from datetime import datetime
from django.forms import ModelForm
from django.views.generic import UpdateView, DeleteView
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.bootstrap import FormActions
from Podo1.context_processors import get_current_group
from journal_views import paginate
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


def employee_list(request):
    current_group = get_current_group(request)
    if current_group:
        employee = Employee.objects.filter (employee_group=current_group)
    else:
        employee = Employee.objects.all()
    # try to order employee list
    order_by = request.GET.get ('order_by', '')
    if order_by in ('last_name', 'first_name', 'level'):
        employee = employee.order_by (order_by)
        if request.GET.get('reverse', '') == '1':
            employee = employee.reverse()

    # apply pagination, 10 employee per page
    context = paginate(employee, 10, request, {},
    var_name ='employee')

    return render (request, 'Prog\\employee\\employee_list.html', context)

"""
class EmployeeList(ListView):
    model = Employee
    context_object_name = 'employees'
    template = 'Prog\\employee\\employee_list.html'

    def get_context_data(self, **kwargs):

        # get original context data from parent class
        context = super(EmployeeList, self).get_context_data(**kwargs)

        # tell template not to show logo on a page
        context['show_logo'] = False

        # return context mapping
        return context

    def get_queryset(self):

        # get original query set
        qs = super(EmployeeList, self).get_queryset()
        # order by last name
        return qs.order_by('last_name')
"""

@login_required
def employee_add(request):
    # was form posted?
    if request.method == "POST":
        # was form add button clicked?
        if request.POST.get ('add_button') is not None:
            errors = {}
            # validate employee data will go here
            data = {'middle_name': request.POST.get ('middle_name'),
                    'notes': request.POST.get ('notes')}
            # validate user input
            first_name = request.POST.get ('first_name', '').strip ()
            if not first_name:
                errors['first_name'] = u"Ім'я є обов'язковим"
            else:
                data['first_name'] = first_name

            last_name = request.POST.get ('last_name', '').strip ()
            if not last_name:
                errors['last_name'] = u"Прізвище є обов'язковим"
            else:
                data['last_name'] = last_name

            birthday = request.POST.get ('birthday', '').strip ()
            if not birthday:
                errors['birthday'] = u"Дата народження є обов'язковою"
            else:
                try:
                    datetime.strptime (birthday, '%Y-%m-%d')
                except Exception:
                    errors['birthday'] = u"Введіть коректний формат дати (напр. 1984 -12 - 30)"
                else:
                    data['birthday'] = birthday

            level = request.POST.get ('level', '').strip ()
            if not level:
                errors['level'] = u"Вкажіть кваліфікацію працівника"
            else:
                data['level'] = level

            employee_group = request.POST.get ('employee_group', '').strip ()
            if not employee_group:
                errors['employee_group'] = u"Оберіть проект для працівника"
            else:
                groups = Group.objects.filter (pk=employee_group)
                if len (groups) != 1:
                    errors['employee_group'] = u"Оберіть коректний проект"
                else:
                    data['employee_group'] = groups[0]

            photo = request.FILES.get ('photo')
            if photo:
                data['photo'] = photo

            if not errors:
                # create employee object
                employee = Employee (
                    first_name=request.POST['first_name'],
                    last_name=request.POST['last_name'],
                    middle_name=request.POST['middle_name'],
                    birthday=request.POST['birthday'],
                    level=request.POST['level'],
                    employee_group=Group.objects.get (pk=request.POST['employee_group']),
                    photo=request.FILES['photo'],
                    notes=request.POST['notes'],
                )
                # save it to database
                employee = Employee (**data)
                employee.save ()

                # redirect user to employees list
                return HttpResponseRedirect (u'%s?status_message=Студента успішно додано!' % reverse ('home'))

            else:
                # render form with errors and previous user input
                return render (request, 'Prog\\employee\\employee_add.html',
                               {'groups': Group.objects.all ().order_by ('title'),
                                'errors': errors})
        elif request.POST.get ('cancel_button') is not None:
            # redirect to home page on cancel button
            return HttpResponseRedirect (u'%s?status_message=Додавання студента скасовано!' % reverse ('home'))
    else:
        # initial form render
        return render (request, 'Prog\\employee\\employee_add.html',
                       {'groups': Group.objects.all ().order_by ('title')})


class EmployeeUpdateForm(ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(EmployeeUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        # set form tag attributes
        self.helper.form_action = reverse('employee_edit', kwargs={'pk': kwargs['instance'].id})
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'
        # set form field properties
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'

        # add buttons
        self.helper.layout[-1] = FormActions(
        Submit('add_button', u'Зберегти', css_class="btn btn-primary"),
        Submit('cancel_button', u'Скасувати', css_class="btn btn-link"),)

class EmployeeUpdateView(UpdateView):
    model = Employee
    template_name = 'Prog\\employee\\employee_edit.html'
    form_class = EmployeeUpdateForm

    @method_decorator (login_required)
    def dispatch(self, *args, **kwargs):
        return super (EmployeeUpdateView, self).dispatch (*args, **kwargs)

    def get_success_url(self):
        return u'%s?status_message=Студента успішно збережено!' % reverse('home')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(u'%s?status_message=Редагування студента відмінено!' % reverse('home'))
        else:
            return super(EmployeeUpdateView, self).post(request, *args, **kwargs)

class EmployeeDeleteView(DeleteView):
    model = Employee
    template_name = 'Prog\employee\employee_delete.html'

    @method_decorator (login_required)
    def dispatch(self, *args, **kwargs):
        return super (EmployeeDeleteView, self).dispatch (*args, **kwargs)

    def get_success_url(self):
        return u'%s?status_message=Студента успішно видалено!' % reverse('home')