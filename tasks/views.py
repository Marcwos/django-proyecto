from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .decorators import UrgentTaskDecorator, ImportantTaskDecorator, NormalTaskDecorator


def home(request):
    return render(request, "home.html")


def signup(request):
    if request.method == 'GET':
        return render(request, "signup.html", {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, "signup.html", {
                        "form": UserCreationForm, 
                        "error": "User already exists"
                        })
            
        return render(request, "signup.html",
                {"form": UserCreationForm, "error": "Password do not match"},
        )

@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    
    decorated_tasks = []
    for task in tasks:
        if task.task_type == 'urgent':
            decorated_tasks.append(UrgentTaskDecorator(task))
        elif task.important:
            decorated_tasks.append(ImportantTaskDecorator(task))
        else:
            decorated_tasks.append(NormalTaskDecorator(task))
    
    return render(request, 'tasks.html', {'tasks': decorated_tasks})

@login_required 
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'completed_task.html', {'tasks': tasks})

@login_required
def create_task(request):
    if request.method == 'GET':
        # Cargar tanto el formulario de tipo de tarea como el formulario principal al mismo tiempo
        return render(request, "create_task.html", {
            'form': TaskForm,
            'task_types': ['normal', 'urgent']  # Lista de tipos de tarea
        })
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user

            # Recibe el valor de 'task_type' desde el formulario
            new_task.task_type = request.POST.get('task_type', 'normal')

            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, "create_task.html", {
                'form': TaskForm,
                'task_types': ['normal', 'urgent'],  # Asegúrate de pasar la lista de tipos de tarea en caso de error
                'error': 'Please provide valid data'
            })


@login_required 
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {'task':task, 'form': form})
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {'task':task, 'form': form, 
                                                        'error': "Error updating task"})

@login_required 
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')

@login_required 
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')

@login_required 
def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST
            ['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Username or password is incorrect'
            })
        else:
            login(request, user)
            return redirect('tasks')
