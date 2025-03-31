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

def itemSaidaView(request):
    template_name = 'include/entrada_items.html'

    if request.method == 'GET':
        form = AddMaterialForm()
        TipoMaterFormset = inlineformset_factory(
            MaterialObj, MaterialTipo, form=TipoMaterForm, extra=1, can_delete=False
        )
        formset = TipoMaterFormset()
        context = {
            'form': form,
            'formset': formset,
        }
        return render(request, template_name, context)

    elif request.method == 'POST':
        form = AddMaterialForm(request.POST)
        TipoMaterFormset = inlineformset_factory(MaterialObj, MaterialTipo, 
                                                 form=TipoMaterForm)
        formset = TipoMaterFormset(request.POST)

        if form.is_valid() and formset.is_valid():
            obj_paiSaved = form.save()
            formset.instance = obj_paiSaved
            formset.save()
            return redirect('entrada_material')
            
        else:
            context = {
                'form': form,
                'formset': formset,
            }
            return render(request, template_name, context)
        
def listarItemsView(request):
    template_name = 'include/listar.html'

    objs = []

    objs_tipo = MaterialObj.objects.prefetch_related('tipo_obj').all()
    
    # items__queryset = MaterialObj.objects.all()
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
        messages.success(request, msgSucesso)
        return redirect('listar_items')


    return request

