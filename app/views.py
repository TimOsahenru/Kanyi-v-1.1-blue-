from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import CleanForm
from .models import Task
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.list import ListView
from django.contrib.auth.views import LoginView
from django.views.generic.detail import DetailView
from django.contrib.auth import login
from django.views.generic.edit import UpdateView, DeleteView, CreateView, FormView
# Create your views here.


class Register(FormView):
    form_class = UserCreationForm
    success_url = reverse_lazy('logout')
    template_name = '../templates/register.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.username = user.username.lower()
        user = form.save()
        if user is not None:
            login(self.request, user)
            return redirect('logout')
        return super(Register, self).form_valid(form)

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('tasklist')
        return super(Register, self).get(request)


class CustomLogin(LoginView):
    template_name = '../templates/login.html'
    redirect_authenticated_user = True
    next_page = 'tasklist'
    form_class = CleanForm


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    template_name = '../templates/taskcreate.html'
    context_object_name = 'task'
    fields = ['title', 'description']
    success_url = reverse_lazy('tasklist')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = '../templates/taskdelete.html'
    context_object_name = 'task'
    success_url = reverse_lazy('tasklist')


class TaskEdit(LoginRequiredMixin, UpdateView):
    model = Task
    template_name = '../templates/taskedit.html'
    context_object_name = 'task'
    fields = ['title', 'description', 'completed']
    success_url = reverse_lazy('tasklist')


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    template_name = '../templates/taskdetail.html'
    context_object_name = 'task'


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    template_name = '../templates/tasklist.html'
    context_object_name = 'tasks'

    def get_context_data(self):
        context = super(TaskList, self).get_context_data()
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(completed=False).count()
        
        search_input = self.request.GET.get('search_area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title_icontains=search_input)
            context['search_input'] = search_input
        return context
    
