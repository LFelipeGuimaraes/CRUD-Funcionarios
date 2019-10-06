from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, UpdateView, DeleteView, CreateView
from employee_management.models import Funcionario
from website.forms import InsereFuncionarioForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from custom_guardian import PermissionRequiredModified # manage permission to a specifc instance of funcionario
from guardian.shortcuts import assign_perm
from django.contrib import messages
from employee_management import settings


# Create your views here.
class IndexTemplateView(TemplateView):
    template_name = 'website/index.html'

def FuncionarioListView(request):
    funcionarios = Funcionario.objects.filter(user__id = request.user.id)
    context = {'funcionarios': funcionarios}
    return render(request=request, template_name='website/lista.html', context=context)


class FuncionarioUpdateView(PermissionRequiredModified, UpdateView):
    # guardian permissions
    permission_required = 'change_funcionario'
    redirect_field_name = ('/funcionarios')

    template_name = 'website/atualiza.html'
    model = Funcionario
    fields = [
        'nome',
        'sobrenome',
        'cpf',
        'tempo_de_servico',
        'remuneracao'
    ]
    success_url = reverse_lazy('website:lista_funcionarios')


class FuncionarioDeleteView(PermissionRequiredModified, DeleteView):
    # guardian permissions
    permission_required = 'delete_funcionario'
    redirect_field_name = ('/funcionarios')

    template_name = 'website/exclui.html'
    model = Funcionario
    context_object_name = 'funcionario'
    success_url = reverse_lazy('website:lista_funcionarios')


@login_required(login_url = '/login')
def FuncionarioCreateView(request):
    if request.method == 'POST':
        form = InsereFuncionarioForm(request.POST)

        if form.is_valid():
            funcionario = form.save(commit=False)
            funcionario.user = request.user
            funcionario.save()

            # assign permissions using guardian
            assign_perm('change_funcionario', request.user, funcionario)
            assign_perm('delete_funcionario', request.user, funcionario)

            return redirect('website:lista_funcionarios')

    form = InsereFuncionarioForm
    return render(request=request, template_name='website/cria.html', context={'form': form})


def request_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request=request, username=username, password=password)
            # se o usuario for autenticado
            if user is not None:
                user.backend = settings.AUTHENTICATION_BACKENDS[0]
                login(request, user)
                return redirect('website:index')
            else:
                for msg in form.error_messages:
                    message.error(request, f'{msg}: {form.error_messages[msg]}')
    
    # se for GET ou usuario nao conseguir autenticar
    # nesse ultimo caso, renderiza a pagina novamente
    form = AuthenticationForm()
    return render(request=request, template_name='website/login.html', context={'form': form})


def register(request):
    if request.method == 'POST':
        print(request.body)
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.backend = settings.AUTHENTICATION_BACKENDS[0]
            login(request, user)
            return redirect('website:index')
        else:
            for msg in form.error_messages:
                messages.error(request, f'{msg}: {form.error_messages[msg]}')

    form = UserCreationForm()
    return render(request=request, template_name='website/register.html', context={'form': form})


def request_logout(request):
    logout(request)
    return redirect('website:index')

