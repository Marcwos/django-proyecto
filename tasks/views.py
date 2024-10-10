from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .decorators import UniversidadTaskDecorator, LaboralTaskDecorator, PersonalTaskDecorator
from .commands import CreateTaskCommand, UpdateTaskCommand, DeleteTaskCommand

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
        if task.task_type == 'university':
            decorated_tasks.append(UniversidadTaskDecorator(task))  
        elif task.task_type == 'personal':
            decorated_tasks.append(PersonalTaskDecorator(task))  
        elif task.task_type == 'work':
            decorated_tasks.append(LaboralTaskDecorator(task))  

    return render(request, 'tasks.html', {'tasks': decorated_tasks})


@login_required 
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'completed_task.html', {'tasks': tasks})

@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, "create_task.html", {
            'form': TaskForm,
            'task_types': ['university', 'personal', 'work']  # Incluye los nuevos tipos aquí
        })
    else:
        try:
            form = TaskForm(request.POST)
            if form.is_valid():
                is_important = request.POST.get('important') == 'True'
                is_soft = request.POST.get('soft') == 'True'

                command = CreateTaskCommand(
                    user=request.user,
                    title=form.cleaned_data['title'],
                    description=form.cleaned_data['description'],
                    task_type=form.cleaned_data['task_type'], 
                    is_important=is_important,
                    is_soft=is_soft
                )
                command.execute()
                return redirect('tasks')
        except ValueError:
            return render(request, "create_task.html", {
                'form': TaskForm,
                'task_types': ['university', 'personal', 'work'],  
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
        command = UpdateTaskCommand(task, datecompleted=timezone.now())
        command.execute()
        return redirect('tasks')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        # Usamos el comando para eliminar la tarea
        command = DeleteTaskCommand(task)
        command.execute()
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
