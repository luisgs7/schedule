from curses import echo
from email import message
from django.shortcuts import redirect, render
from django.contrib import messages, auth
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def login(request):
    if request.method != 'POST':
        return render(request, 'accounts/login.html')

    usuario = request.POST.get('usuario')
    password = request.POST.get('senha')

    user = auth.authenticate(request, username=usuario, password=password)

    if not user:
        messages.error(request, 'Usuário ou senha inválidos.')
        return render(request, 'accounts/login.html')

    else:
        auth.login(request, user)
        messages.success(request, 'Login realizado com Sucesso.')
        return redirect('dashboard')

def logout(request):
    auth.logout(request)
    return redirect('login')


def cadastro(request):
    #messages.success(request, 'Olá mundo')
    #print(request.POST)
    if request.method != 'POST':
        return render(request, 'accounts/cadastro.html')

    nome = request.POST.get('nome') 
    sobrenome = request.POST.get('sobrenome') 
    usuario = request.POST.get('usuario') 
    email = request.POST.get('email') 
    usuario = request.POST.get('usuario') 
    senha = request.POST.get('senha') 
    senha2 = request.POST.get('senha2') 

    if not nome or not sobrenome or not email or not usuario \
        or not senha or not senha2:
        messages.error(request, 'Nehum campo pode estar vazio.')
        return render(request, 'accounts/cadastro.html')

    try:
        validate_email(email)
    except:
        messages.error(request, 'Email inválido.')
        return render(request, 'accounts/cadastro.html')
    
    if len(senha) < 6:
        messages.error(request, 'Senha precisa ter 6 caracteres ou mais.')
        return render(request, 'accounts/cadastro.html')
    
    if len(usuario) < 6:
        messages.error(request, 'Usuário precisa ter 6 caracteres ou mais.')
        return render(request, 'accounts/cadastro.html')
    
    if senha != senha2:
        messages.error(request, 'Senhas não conferem.')
        return render(request, 'accounts/cadastro.html')
    
    if User.objects.filter(username=usuario).exists():
        messages.error(request, 'Usuário já existe.')
        return render(request, 'accounts/cadastro.html')
    
    if User.objects.filter(email=email).exists():
        messages.error(request, 'E-mail já existe.')
        return render(request, 'accounts/cadastro.html')

    messages.success(request, 'Registrado com sucesso! Agora faça Login.')

    user = User.objects.create_user(username=usuario, email=email,
                                    password=senha, first_name=nome,
                                    last_name=sobrenome)
    user.save()
    return redirect('login')


@login_required(redirect_field_name='login')
def dashboard(request):
    return render(request, 'accounts/dashboard.html')