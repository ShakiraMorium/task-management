# from django.shortcuts import render, redirect
# from django.http import HttpResponse
# from tasks.forms import TaskForm, TaskModelForm, TaskDetailModelForm
# from tasks.models import Task, TaskDetail, Project
# from datetime import date
# from django.db.models import Q, Count, Max, Min, Avg
# from django.contrib import messages
# from django.contrib.auth.decorators import user_passes_test, login_required, permission_required
# from users.views import is_admin
# from django.http import HttpResponse
# from django.views import View
# from django.utils.decorators import method_decorator
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib.auth.mixins import PermissionRequiredMixin
# from django.views.generic.base import ContextMixin
# from django.views.generic import ListView, DetailView, UpdateView
# from django.views import View

# # Class Based View Re-use example


# class Greetings(View):
#     greetings = 'Hello Everyone'

#     def get(self, request):
#         return HttpResponse(self.greetings)


# class HiGreetings(Greetings):
#     greetings = 'Hi Everyone'


# class HiHowGreetings(Greetings):
#     greetings = 'Hi Everyone, How are you'


# def is_manager(user):
#     return user.groups.filter(name='Manager').exists()


# def is_employee(user):
#     return user.groups.filter(name='Manager').exists()


# @user_passes_test(is_manager, login_url='no-permission')
# def manager_dashboard(request):

#     # getting task count
#     # total_task = tasks.count()
#     # completed_task = Task.objects.filter(status="COMPLETED").count()
#     # in_progress_task = Task.objects.filter(status='IN_PROGRESS').count()
#     # pending_task = Task.objects.filter(status="PENDING").count()

#     # count = {
#     #     "total_task":
#     #     "completed_task":
#     #     "in_progress_task":
#     #     "pending_task":
#     # }
#     type = request.GET.get('type', 'all')
#     # print(type)

#     counts = Task.objects.aggregate(
#         total=Count('id'),
#         completed=Count('id', filter=Q(status='COMPLETED')),
#         in_progress=Count('id', filter=Q(status='IN_PROGRESS')),
#         pending=Count('id', filter=Q(status='PENDING')),
#     )

#     # Retriving task data

#     base_query = Task.objects.select_related(
#         'details').prefetch_related('assigned_to')

#     if type == 'completed':
#         tasks = base_query.filter(status='COMPLETED')
#     elif type == 'in-progress':
#         tasks = base_query.filter(status='IN_PROGRESS')
#     elif type == 'pending':
#         tasks = base_query.filter(status='PENDING')
#     elif type == 'all':
#         tasks = base_query.all()

#     context = {
#         "tasks": tasks,
#         "counts": counts,
#         "role": 'manager'
#     }
#     return render(request, "dashboard/manager-dashboard.html", context)


# @user_passes_test(is_employee)
# def employee_dashboard(request):
#     return render(request, "dashboard/user-dashboard.html")


# @login_required
# @permission_required("tasks.add_task", login_url='no-permission')
# def create_task(request):
#     # employees = Employee.objects.all()
#     task_form = TaskModelForm()  # For GET
#     task_detail_form = TaskDetailModelForm()

#     if request.method == "POST":
#         task_form = TaskModelForm(request.POST)
#         task_detail_form = TaskDetailModelForm(request.POST, request.FILES)

#         if task_form.is_valid() and task_detail_form.is_valid():

#             """ For Model Form Data """
#             task = task_form.save()
#             task_detail = task_detail_form.save(commit=False)
#             task_detail.task = task
#             task_detail.save()

#             messages.success(request, "Task Created Successfully")
#             return redirect('create-task')

#     context = {"task_form": task_form, "task_detail_form": task_detail_form}
#     return render(request, "task_form.html", context)


# # variable for list of decorators
# create_decorators = [login_required, permission_required(
#     "tasks.add_task", login_url='no-permission')]


# class CreateTask(ContextMixin, LoginRequiredMixin, PermissionRequiredMixin, View):
#     """ For creating task """
#     permission_required = 'tasks.add_task'
#     login_url = 'sign-in'
#     template_name = 'task_form.html'

#     """ 
#     0. Create Task
#     1. LoginRequiredMixin
#     2. PermissionRequiredMixin
#     """

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['task_form'] = kwargs.get('task_form', TaskModelForm())
#         context['task_detail_form'] = kwargs.get(
#             'task_detail_form', TaskDetailModelForm())
#         return context

#     def get(self, request, *args, **kwargs):
#         context = self.get_context_data()
#         return render(request, self.template_name, context)

#     def post(self, request, *args, **kwargs):
#         task_form = TaskModelForm(request.POST)
#         task_detail_form = TaskDetailModelForm(request.POST, request.FILES)

#         if task_form.is_valid() and task_detail_form.is_valid():

#             """ For Model Form Data """
#             task = task_form.save()
#             task_detail = task_detail_form.save(commit=False)
#             task_detail.task = task
#             task_detail.save()

#             messages.success(request, "Task Created Successfully")
#             context = self.get_context_data(
#                 task_form=task_form, task_detail_form=task_detail_form)
#             return render(request, self.template_name, context)


# @login_required
# @permission_required("tasks.change_task", login_url='no-permission')
# def update_task(request, id):
#     task = Task.objects.get(id=id)
#     task_form = TaskModelForm(instance=task)  # For GET

#     if task.details:
#         task_detail_form = TaskDetailModelForm(instance=task.details)

#     if request.method == "POST":
#         task_form = TaskModelForm(request.POST, instance=task)
#         task_detail_form = TaskDetailModelForm(
#             request.POST, request.Files, instance=task.details)

#         if task_form.is_valid() and task_detail_form.is_valid():

#             """ For Model Form Data """
#             task = task_form.save()
#             task_detail = task_detail_form.save(commit=False)
#             task_detail.task = task
#             task_detail.save()

#             messages.success(request, "Task Updated Successfully")
#             return redirect('update-task', id)

#     context = {"task_form": task_form, "task_detail_form": task_detail_form}
#     return render(request, "task_form.html", context)


# class UpdateTask(UpdateView):
#     model = Task
#     form_class = TaskModelForm
#     template_name = 'task_form.html'
#     context_object_name = 'task'
#     pk_url_kwarg = 'id'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['task_form'] = self.get_form()
#         # print(context)
#         if hasattr(self.object, 'details') and self.object.details:
#             context['task_detail_form'] = TaskDetailModelForm(
#                 instance=self.object.details)
#         else:
#             context['task_detail_form'] = TaskDetailModelForm()

#         return context

#     def post(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         task_form = TaskModelForm(request.POST, instance=self.object)

#         task_detail_form = TaskDetailModelForm(
#             request.POST, request.FILES, instance=getattr(self.object, 'details', None))

#         if task_form.is_valid() and task_detail_form.is_valid():

#             """ For Model Form Data """
#             task = task_form.save()
#             task_detail = task_detail_form.save(commit=False)
#             task_detail.task = task
#             task_detail.save()

#             messages.success(request, "Task Updated Successfully")
#             return redirect('update-task', self.object.id)
#         return redirect('update-task', self.object.id)


# @login_required
# @permission_required("tasks.delete_task", login_url='no-permission')
# def delete_task(request, id):
#     if request.method == 'POST':
#         task = Task.objects.get(id=id)
#         task.delete()
#         messages.success(request, 'Task Deleted Successfully')
#         return redirect('manager-dashboard')
#     else:
#         messages.error(request, 'Something went wrong')
#         return redirect('manager-dashboard')


# @login_required
# @permission_required("tasks.view_task", login_url='no-permission')
# def view_task(request):
#     projects = Project.objects.annotate(
#         num_task=Count('task')).order_by('num_task')
#     return render(request, "show_task.html", {"projects": projects})


# view_project_decorators = [login_required, permission_required(
#     "projects.view_project", login_url='no-permission')]


# @method_decorator(view_project_decorators, name='dispatch')
# class ViewProject(ListView):
#     model = Project
#     context_object_name = 'projects'
#     template_name = 'show_task.html'

#     def get_queryset(self):
#         queryset = Project.objects.annotate(
#             num_task=Count('task')).order_by('num_task')
#         return queryset


# @login_required
# @permission_required("tasks.view_task", login_url='no-permission')
# def task_details(request, task_id):
#     task = Task.objects.get(id=task_id)
#     status_choices = Task.STATUS_CHOICES

#     if request.method == 'POST':
#         selected_status = request.POST.get('task_status')
#         # print(selected_status)
#         task.status = selected_status
#         task.save()
#         return redirect('task-details', task.id)

#     return render(request, 'task_details.html', {"task": task, 'status_choices': status_choices})


# class TaskDetail(DetailView):
#     model = Task
#     template_name = 'task_details.html'
#     context_object_name = 'task'
#     pk_url_kwarg = 'task_id'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)  # {"task": task}
#         # {"task": task, 'status_choices': status_choices}
#         context['status_choices'] = Task.STATUS_CHOICES
#         return context

#     def post(self, request, *args, **kwargs):
#         task = self.get_object()
#         selected_status = request.POST.get('task_status')
#         task.status = selected_status
#         task.save()
#         return redirect('task-details', task.id)


# @login_required
# def dashboard(request):
#     if is_manager(request.user):
#         return redirect('manager-dashboard')
#     elif is_employee(request.user):
#         return redirect('user-dashboard')
#     elif is_admin(request.user):
#         return redirect('admin-dashboard')

#     return redirect('no-permission')




# class-based-view

# Converted all function-based views into class-based views (CBV)

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from tasks.forms import TaskModelForm, TaskDetailModelForm
from tasks.models import Task, TaskDetail, Project
from django.db.models import Q, Count
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.views.generic import View, TemplateView, ListView, DetailView, UpdateView, DeleteView

# Helper functions
def is_manager(user):
    return user.groups.filter(name='Manager').exists()

def is_employee(user):
    return user.groups.filter(name='Employee').exists()

# Dashboard Views
class ManagerDashboard(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "dashboard/manager-dashboard.html"

    def test_func(self):
        return is_manager(self.request.user)

    def handle_no_permission(self):
        return redirect('no-permission')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        type = self.request.GET.get('type', 'all')

        counts = Task.objects.aggregate(
            total=Count('id'),
            completed=Count('id', filter=Q(status='COMPLETED')),
            in_progress=Count('id', filter=Q(status='IN_PROGRESS')),
            pending=Count('id', filter=Q(status='PENDING')),
        )

        base_query = Task.objects.select_related('details').prefetch_related('assigned_to')
        if type == 'completed':
            tasks = base_query.filter(status='COMPLETED')
        elif type == 'in-progress':
            tasks = base_query.filter(status='IN_PROGRESS')
        elif type == 'pending':
            tasks = base_query.filter(status='PENDING')
        else:
            tasks = base_query.all()

        context.update({"tasks": tasks, "counts": counts, "role": "manager"})
        return context

class EmployeeDashboard(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "dashboard/user-dashboard.html"

    def test_func(self):
        return is_employee(self.request.user)

# Task Creation
class CreateTask(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'tasks.add_task'
    login_url = 'sign-in'
    template_name = 'task_form.html'

    def get(self, request):
        context = {
            'task_form': TaskModelForm(),
            'task_detail_form': TaskDetailModelForm(),
        }
        return render(request, self.template_name, context)

    def post(self, request):
        task_form = TaskModelForm(request.POST)
        task_detail_form = TaskDetailModelForm(request.POST, request.FILES)

        if task_form.is_valid() and task_detail_form.is_valid():
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()
            messages.success(request, "Task Created Successfully")
            return redirect('create-task')

        context = {'task_form': task_form, 'task_detail_form': task_detail_form}
        return render(request, self.template_name, context)

# Task Update
class UpdateTaskCBV(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'tasks.change_task'
    login_url = 'sign-in'
    template_name = 'task_form.html'

    def get(self, request, id):
        task = get_object_or_404(Task, id=id)
        task_form = TaskModelForm(instance=task)
        task_detail_form = TaskDetailModelForm(instance=task.details if hasattr(task, 'details') else None)
        return render(request, self.template_name, {'task_form': task_form, 'task_detail_form': task_detail_form})

    def post(self, request, id):
        task = get_object_or_404(Task, id=id)
        task_form = TaskModelForm(request.POST, instance=task)
        task_detail_form = TaskDetailModelForm(request.POST, request.FILES, instance=task.details if hasattr(task, 'details') else None)

        if task_form.is_valid() and task_detail_form.is_valid():
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()
            messages.success(request, "Task Updated Successfully")
            return redirect('update-task', id=id)

        return render(request, self.template_name, {'task_form': task_form, 'task_detail_form': task_detail_form})

# Task Delete
class DeleteTask(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'tasks.delete_task'
    login_url = 'sign-in'

    def post(self, request, id):
        task = get_object_or_404(Task, id=id)
        task.delete()
        messages.success(request, 'Task Deleted Successfully')
        return redirect('manager-dashboard')

# View Tasks by Project
class ViewTaskByProject(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Project
    template_name = 'show_task.html'
    context_object_name = 'projects'
    permission_required = 'tasks.view_task'

    def get_queryset(self):
        return Project.objects.annotate(num_task=Count('task')).order_by('num_task')

# Task Detail View
class TaskDetailsCBV(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Task
    template_name = 'task_details.html'
    context_object_name = 'task'
    pk_url_kwarg = 'task_id'
    permission_required = 'tasks.view_task'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = Task.STATUS_CHOICES
        return context

    def post(self, request, *args, **kwargs):
        task = self.get_object()
        selected_status = request.POST.get('task_status')
        task.status = selected_status
        task.save()
        return redirect('task-details', task.id)

# Main Dashboard Redirect View
class DashboardRedirect(LoginRequiredMixin, View):
    def get(self, request):
        if is_manager(request.user):
            return redirect('manager-dashboard')
        elif is_employee(request.user):
            return redirect('user-dashboard')
        elif request.user.is_superuser:
            return redirect('admin-dashboard')
        return redirect('no-permission')

