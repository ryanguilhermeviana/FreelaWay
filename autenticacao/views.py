from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages 
from django.contrib.messages import constants 
from django.contrib.auth import authenticate, login, logout


def cadastro(request):
    if request.method == "GET": 
        if request.user.is_authenticated:
            return redirect('home/')
        return render(request, 'autenticacao/cadastro.html') 
    
    elif request.method == "POST": 
        username = request.POST.get('username') 
        senha = request.POST.get('password') 
        confirmar_senha = request.POST.get('confirm-password') 

        if not senha == confirmar_senha: 
            messages.add_message(request, constants.ERROR, 
                                 'As senhas não coincidem')
            return redirect('/auth/cadastro') 
        
        if len(username.strip()) == 0 or len(senha.strip()) == 0:
            messages.add_message(request, constants.ERROR, 
                                 'Preencha todos os campos') 
            return redirect('/auth/cadastro') 
        
        user = User.objects.filter(username=username) 

        if user.exists(): 
            messages.add_message(request, constants.ERROR, 
                                 'Já existe um usário com esse username')
            return redirect('/auth/cadastro')
        
        try: 
            user = User.objects.create_user(username=username, 
                                            password=senha) 
            user.save() 
            messages.add_message(request, constants.SUCCESS, 
                                 'Usuário criado com sucesso')
            return redirect('/auth/logar') 
        except: 
            messages.add_message(request, constants.ERROR, 
                                 'Erro interno do sistema') 
            return redirect('/auth/cadastro')

def logar(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('home/')
        return render(request, 'autenticacao/logar.html')
    
    username = request.POST.get('username')
    senha = request.POST.get('password')

    usuario = authenticate(username=username, password=senha)

    if not usuario:
        messages.add_message(request, constants.ERROR, 
                             'Username ou senha inválidos') 
        return redirect('/auth/logar')
    
    login(request, usuario)
    return redirect('home/')


def sair(request):
    logout(request)
    return redirect('logar')
