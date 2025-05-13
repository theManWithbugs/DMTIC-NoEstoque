from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from . forms import *
from . models import *
from . utils import *
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.forms import inlineformset_factory
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UnidadeSerializer, DepartamentoSerializer, DivisaoSerializer
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.db import IntegrityError
from collections import Counter

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

@login_required
def baseView(request):
    template_name = 'base.html'
    return render(request, template_name)

@login_required
def homeView(request):
    template_name = 'include/home.html'
    dados = receber_dados(request)
    return render(request, template_name)

def logoutView(request):
    auth_logout(request)
    return redirect('login_page')

@login_required
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

@login_required
def inserirItem(request): 
    template_name = 'include/inse_item.html'
    form = AddMaterialForm(request.POST or None)

    if request.method == 'POST':

        if form.is_valid():
            form.save()
            messages.success(request, msgSucesso)
            return redirect('new_item')

    return render(request, template_name, {'form': form})

@login_required
def save_formset(formset):
    for form in formset:
        if form.is_valid() and form.has_changed():
            form.save()

@login_required
def itemAddView(request):
    template_name = 'include/entrada_items.html'

    TipoMaterFormset = inlineformset_factory(
        MaterialObj, MaterialTipo, form=TipoMaterForm, 
        extra=3, can_delete=False
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
                HistoricoUser.objects.create(
                    nome_user = request.user.first_name,
                    acao_realizada = 'Entrada de item'
                )
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
        
@login_required
def listarItemsView(request):
    template_name = 'include/listar.html'

    marca_modelo = Counter()

    objs = []

    objs_tipo = MaterialObj.objects.prefetch_related('tipo_obj')

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

    for obj in objs:
        for obj_inside in obj.tipo_obj.all():
            if obj_inside.marca and obj_inside.modelo:
                marca_modelo[( f"( Marca: {obj_inside.marca} ) ( Modelo: {obj_inside.modelo} ) ")] += 1

    context = {
        'objs': objs,
        'marca_modelo': marca_modelo,
    }

    return render(request, template_name, context)

@login_required
def itemSaidaViewLista(request):
    template_name = 'include/listar_saida.html' 

    unidade = None
    departmento = None
    divisao = None

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

    for obj in objs:
        unidade = str(obj.unidade).split(" ")[0]
        departmento = str(obj.departamento).split(" ")[0]
        divisao = str(obj.divisao_field).split(" ")[0]

    context = {
        'objs': objs,
        'unidade': unidade,
        'departamento': departmento,
        'divisao': divisao,
    }

    return render(request, template_name, context)

@login_required
def noExitItemsView(request):
    template_name = 'include/listar_dispo.html'
    
    objs = []

    objs_tipo = MaterialObj.objects.prefetch_related('tipo_obj')

    paginator = Paginator(objs_tipo, 14)
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

@login_required
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

@login_required
def addContratoView(request):  
    template_name = 'include/add_contrato.html'
    form = AddContratoForm(request.POST or None)  

    if request.method == 'POST':

        if form.is_valid():
            form.save()
            messages.success(request, 'Operação realizada com sucesso!')
            return redirect('add_contr')
        else:
            messages.error(request, 'Não foi possível realizar!')

    return render(request, template_name, {'form': form})

@login_required
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

@login_required
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

@login_required
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

@login_required
def filtro_view(request, id):

    unidade_id = request.GET.get('unidade') 
    departamento_id = request.GET.get('departamento')  
    divisao_id = request.GET.get('divisao') 
    n_processo = request.GET.get('n_processo')

    if unidade_id and departamento_id and divisao_id:

        try:
            unidade = Unidade.objects.get(id=unidade_id)
            departamento = Departamento.objects.get(id=departamento_id)
            divisao = Divisao.objects.get(id=divisao_id)
            n_processo = MaterialSaida.objects.get(n_processo=n_processo)
        except ObjectDoesNotExist:
            pass

        if request.method == 'GET':
            saida = MaterialSaida.objects.create(
                    unidade=unidade,
                    departamento=departamento,
                    divisao_field=divisao,
                    n_processo=n_processo,
                )
            messages.success(request, "MaterialSaida criado com sucesso!")

    try:
        material_tipo = get_object_or_404(MaterialTipo, id=id)
        material_tipo.saida_obj = saida
        material_tipo.save()
        return redirect('listar_items')
    except NameError:
        pass

    context = {
        'form': FiltroForm(
            unidade_id=unidade_id,
            departamento_id=departamento_id,
            divisao_id=divisao_id,
            data=request.GET
        ),
        'material_tipo': material_tipo,
    }

    return render(request, 'include/criar_saida_filtro.html', context)

class jsFiltroJson(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        unidades = Unidade.objects.all()

        departamentos = Departamento.objects.prefetch_related('unidade')

        divisoes = Divisao.objects.all()

        unidades_serialized = UnidadeSerializer(unidades, 
                                                many=True).data
        
        departamentos_serialized = DepartamentoSerializer(departamentos, 
                                                          many=True).data
        
        divisoes_serialized = DivisaoSerializer(divisoes, 
                                                many=True).data

        return Response({
            'unidades': unidades_serialized,
            'departamentos': departamentos_serialized,
            'divisoes': divisoes_serialized,
        })

@login_required
def testeJsFiltroView(request):
    template_name = 'include/teste_filtrojs.html'

    unidades = Unidade.objects.all()
    departamentos = Departamento.objects.all()
    divisoes = Divisao.objects.all()

    context = {
        'unidades': unidades,
        'departamentos': departamentos,
        'divisoes': divisoes,
    }

    return render(request, template_name, context)

def EstatisticasView(request):
    template_name = 'include/estatisticas.html'
    return render(request, template_name)

def teste_async(request):
    dados_unidade = get_estatisticas_unidades(request)
    return JsonResponse(dados_unidade, safe=False)

def teste_async_two(request):
    dados_departamento = get_estatisticas_departmentos(request)
    return JsonResponse(dados_departamento, safe=False)

def dados_items(request):
    items_info = item_agrupados(request)
    return JsonResponse(items_info, safe=False)

def materiais_info(request):
    data = 'Envio funcionando!'
    return JsonResponse(data, safe=False)



