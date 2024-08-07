from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
#from .models import massage
# Create your views here.


def home(request):
    return render(request, 'todo/home.html')

def signupuser(request):
    if request.method == 'GET':
        return render(request, 'todo\signup.html', {'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            # Create new user
            try:
                user = User.objects.create_user(request.POST['username'], password = request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currenttodos')
            except IntegrityError:
                return render(request, 'todo\signup.html', {'form':UserCreationForm(), 'error':'Это имя пользователя уже используется'})
        else:
            # Password1 and Password2 didnt match
            return render(request, 'todo\signup.html', {'form':UserCreationForm(), 'error':'Error'})

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todo\loginuser.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo\loginuser.html', {'form':AuthenticationForm(), 'error':'Этот Логин и/или Пароль введены не верно!'})
        else:
            login(request, user)
            return redirect('currenttodos')

def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


def currenttodos(request):
    todo = Todo.objects.filter(user = request.user, datecompleted__isnull = True)
    return render(request, 'todo\currenttodos.html', {'todo':todo})

def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html', {'form' : TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodos', )
        except ValueError:
            return render(request, 'todo/createtodo.html', {'form' : TodoForm(), 'error': 'Неверное кол-во символов'})


def viewtodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user = request.user)
    if request.method == 'GET':
        form = TodoForm (instance=todo)
        return render(request, 'todo/viewtodo.html', {'todo': todo, 'form':form} )
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos',) 
        except ValueError:
            return render(request, 'todo/createtodo.html', {'form' : TodoForm(), 'error': 'Неверное кол-во символов'})


def completetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user = request.user)
    if request.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('currenttodos') 
    
def deletetodo(request, todo_pk):
#    todo = get_object_or_404(Todo, pk=todo_pk, user = request.user)
    todo = Todo.objects.get(id = todo_pk)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos',) 

def complitetodolist(request):
    todo = Todo.objects.filter(user = request.user, datecompleted__isnull = False).order_by('-datecompleted')

 #   todo = Todo.objects.filter(user = request.user, datecompleted__isnull = True)
    return render(request, 'todo\complitetodolist.html', {'todo': todo})
 #   return redirect(request 'currenttodos', complete_todo)


'''
def massage_user(request):
    massage = Massage.objects.filter(login=user)
    '''
