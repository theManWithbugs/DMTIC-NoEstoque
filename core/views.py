from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as auth_logout
from . forms import *
from django.contrib import messages
from . models import *
from django.http import JsonResponse
from . utils import *
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.forms import inlineformset_factory

msgSucesso = 'Operação realizada com sucesso!'
msgError = 'Ambos os campos devem ser preenchidos!'
msgIntegridade = 'Você tentou salvar um registro que já existe! Por favor, verifique e tente novamente.'
msgCPF = 'CPF deve conter apenas números!'

def loginView(request):
    template_name = 'account/login.html'

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Login ou senha incorretos!')
  
    return render(request, template_name)

def baseView(request):
    template_name = 'base.html'
    return render(request, template_name)

def homeView(request):
    template_name = 'include/home.html'
    return render(request, template_name)

def logoutView(request):
    auth_logout(request)
    return redirect('login_page')

def addUnidadeView(request):
    template_name = 'include/add_unidade.html'
    form = AddUnidadeForm(request.POST or None)
    form_dep = AddDepartForm(request.POST or None)
    form_divis = AddDivisãoForm(request.POST or None)
        
    if request.method == 'POST':

        if 'unidade_submit' in request.POST and form.is_valid():
            form.save()
            messages.success(request, msgSucesso)
            return redirect('add_unidade')

        elif form_dep.is_valid():
            form_dep.save()
            messages.success(request, msgSucesso)
            return redirect('add_unidade')

        elif form_divis.is_valid():
            form_divis.save()
            messages.success(request, msgSucesso)
            return redirect('add_unidade')
        
    context = {
        'form': form,
        'form_dep': form_dep,
        'form_divis': form_divis,
    }

    return render(request, template_name, context)

def inserirItem(request): 
    template_name = 'include/inse_item.html'
    form = AddMaterialForm(request.POST or None)

    if request.method == 'POST':

        if form.is_valid():
            form.save()
            messages.success(request, msgSucesso)
            return redirect('new_item')

    return render(request, template_name, {'form': form})

def save_formset(formset):
    for form in formset:
        if form.is_valid() and form.has_changed():
            form.save()

def itemAddView(request):
    template_name = 'include/entrada_items.html'

    TipoMaterFormset = inlineformset_factory(
        MaterialObj, MaterialTipo, form=TipoMaterForm, extra=3, can_delete=False
    )

    if request.method == 'GET':
        form = AddMaterialForm()
        formset = TipoMaterFormset()
        context = {
            'form': form,
            'formset': formset,
        }
        return render(request, template_name, context)

    elif request.method == 'POST':
        form = AddMaterialForm(request.POST)
        if form.is_valid():
            obj_paiSaved = form.save()

            formset = TipoMaterFormset(request.POST, instance=obj_paiSaved)

            if formset.is_valid():
                formset.save()
                messages.success(request, "Itens salvos com sucesso!")
                return redirect('listar_items')
            else:
                messages.error(request, "Erro ao salvar os itens do formset.")
        else:
            formset = TipoMaterFormset(request.POST)
            messages.error(request, "Erro ao salvar o formulário principal.")

        context = {
            'form': form,
            'formset': formset,
        }
        return render(request, template_name, context)
        
def listarItemsView(request):
    template_name = 'include/listar.html'

    objs = []

    objs_tipo = MaterialObj.objects.prefetch_related('tipo_obj')

    paginator = Paginator(objs_tipo, 4)
    page = request.GET.get('page')

    try:    
        objs = paginator.page(page)
    except PageNotAnInteger:
        objs = paginator.page(1)
    except EmptyPage:
        objs = paginator.page(paginator.num_pages)

    if objs.object_list.exists():
        pass

    context = {
        'objs': objs,
    }

    return render(request, template_name, context)

def itemSaidaViewLista(request):
    template_name = 'include/listar_saida.html' 

    objs = []

    objs_tipo = MaterialSaida.objects.prefetch_related('saida_obj')  

    paginator = Paginator(objs_tipo, 10)
    page = request.GET.get('page')

    try:    
        objs = paginator.page(page)
    except PageNotAnInteger:
        objs = paginator.page(1)
    except EmptyPage:
        objs = paginator.page(paginator.num_pages)

    if objs.object_list.exists():
        pass

    context = {
        'objs': objs,
    }

    return render(request, template_name, context)

def noExitItemsView(request):
    template_name = 'include/listar_dispo.html'
    
    objs = []

    objs_tipo = MaterialObj.objects.prefetch_related('tipo_obj')

    paginator = Paginator(objs_tipo, 4)
    page = request.GET.get('page')

    try:    
        objs = paginator.page(page)
    except PageNotAnInteger:
        objs = paginator.page(1)
    except EmptyPage:
        objs = paginator.page(paginator.num_pages)

    if objs.object_list.exists():
        pass

    context = {
        'objs': objs,
    }

    return render(request, template_name, context)

def editarItemsView(request, id):
    template_name = 'include/edit_material.html'

    item = get_object_or_404(MaterialTipo, id=id)
    
    if request.method == 'POST':

        form = EditarMaterialForm(request.POST, instance=item)

        if form.is_valid():
            form.save()
            messages.success(request, msgSucesso)
            return redirect('listar_items')
        else:
            messages.error(request, msgError)

    else:
        form = EditarMaterialForm(instance=item)
    
    context = {
        'form': form,
    }
    
    return render(request, template_name, context)

def addContratoView(request):  
    template_name = 'include/add_contrato.html'
    form = AddContratoForm(request.POST or None)  

    if request.method == 'POST':

        if form.is_valid():
            form.save()
            messages.success(request, 'Operação realizada com sucesso!')
            return redirect('add_contr')

    return render(request, template_name, {'form': form})

def excluirItems(request, id):

    item = get_object_or_404(MaterialTipo, id=id)

    if item:
        item.delete()
        HistoricoUser.objects.create(
                nome_user = request.user.first_name,
                acao_realizada = 'Exclusão de item'
            )
        messages.success(request, msgSucesso)
        return redirect('itens_disponiveis')

    return request

def saida_ItemView(request, id):
    template_name = 'include/saida_obj.html'

    material_tipo = get_object_or_404(MaterialTipo, id=id)

    if not material_tipo.saida_obj:
        return redirect('create_material_saida', material_tipo_id=material_tipo.id)

    material_saida = material_tipo.saida_obj

    if request.method == 'POST':
        form = SaidaMaterialForm(request.POST, instance=material_saida)
        if form.is_valid():
            form.save()
            HistoricoUser.objects.create(
                nome_user = request.user.first_name,
                acao_realizada = 'Atualização de saida',
                modelo_item = material_tipo.modelo
            )
            messages.success(request, "Atualizado com sucesso!")
            return redirect('listar_items')  
        else:
            messages.error(request, msgError)
    else:
        form = SaidaMaterialForm(instance=material_saida)

    context = {
        'form': form,
        'material_tipo': material_tipo,
    }

    return render(request, template_name, context)

def create_material_saida(request, material_tipo_id):
    template_name = 'include/create_material_saida.html'

    material_tipo = get_object_or_404(MaterialTipo, id=material_tipo_id)

    if request.method == 'POST':
        form = SaidaMaterialForm(request.POST)
        if form.is_valid():
            material_saida = form.save()
            material_tipo.saida_obj = material_saida
            material_tipo.save()
            HistoricoUser.objects.create(
                nome_user = request.user.first_name,
                acao_realizada = 'Saida de material',
                modelo_item = material_tipo.modelo
            )
            messages.success(request, msgSucesso)
            return redirect('listar_items')
    else:
        form = SaidaMaterialForm()

    context = {
        'form': form,
        'material_tipo': material_tipo,
    }

    return render(request, template_name, context)

def histUsuarioView(request):
    template_name = 'include/hist_usuario.html'

    user = HistoricoUser.objects.all()

    objs = []

    objs_tipo = HistoricoUser.objects.all()

    paginator = Paginator(objs_tipo, 10)
    page = request.GET.get('page')

    try:    
        objs = paginator.page(page)
    except PageNotAnInteger:
        objs = paginator.page(1)
    except EmptyPage:
        objs = paginator.page(paginator.num_pages)

    if objs.object_list.exists():
        pass

    context = {
        'user': user,
        'objs': objs,
    }

    return render(request, template_name, context)

def filtro_view(request):
    unidade_id = request.GET.get('unidade')  
    departamento_id = request.GET.get('departamento')  

    form = FiltroForm(
        unidade_id=unidade_id,
        departamento_id=departamento_id,
        data=request.GET  
    )

    context = {
        'form': form,
    }
    return render(request, 'include/teste.html', context)



