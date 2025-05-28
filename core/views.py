from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.forms import inlineformset_factory
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UnidadeSerializer, DepartamentoSerializer, DivisaoSerializer, DepartamentoCountSerializer
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from collections import Counter
from django.db import IntegrityError
from django.db.models import Count
from collections import defaultdict
from . forms import *
from . models import *
from . utils import *

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

    active = False;

    if active == True:
        agrupados_por_departamento= defaultdict(list)

        material_tipos = MaterialTipo.objects.select_related('saida_obj__departamento').all()

        for item in material_tipos:

            departamento = item.saida_obj.departamento.nome if item.saida_obj and item.saida_obj.departamento else "Sem Departamento"

            agrupados_por_departamento[departamento].append(item.get_complete_object())

        resultado = []

        for departamento, itens in agrupados_por_departamento.items():
            resultado.append({
                "Departamento": departamento,
                "itens": itens
                })
            
        linhas = []
        for dep in resultado:
            departamento = dep["Departamento"]
            for item in dep["itens"]:
                saida = item["Saida"]
                unidade = saida.split('-')[1] if saida else ""
                linhas.append({
                    "Departamento": departamento,
                    "Unidade": unidade,
                    "Marca": item["Marca"],
                    "Modelo": item["Modelo"],
                    "Número de série": item["Número de série"],
                    "Patrimonio": item["Patrimonio"],
                    "Observação": item["Observação"],
                    "Garantia": item["Garantia"],
                })

            df = pd.DataFrame(linhas)

            # Cria um buffer em memória
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Itens')

            buffer.seek(0)

        response = HttpResponse(
            buffer,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="itens_departamentos.xlsx"'
        return response

    dados = MaterialSaida.objects.all()

    contagem_departamentos = (
        MaterialSaida.objects.values('departamento__nome')
        .annotate(total=Count('departamento'))
        .order_by('departamento__nome')
    )

    result = receber_dados_departamento(request)

    context = {
        'dados': dados,
        'contagem_departamentos': contagem_departamentos,
    }

    return render(request, template_name, context)

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
            try:
                form.save()
                messages.success(request, msgSucesso)
                return redirect('add_unidade')
            except IntegrityError:
                messages.error(request, msgIntegridade)
                return redirect('add_unidade')

        elif form_dep.is_valid():
            try:
                form_dep.save()
                messages.success(request, msgError)
                return redirect('add_unidade')
            except IntegrityError:
                messages.error(request, msgIntegridade)
                return redirect('add_unidade')

        elif form_divis.is_valid():
            try:
                form_divis.save()
                messages.success(request, msgSucesso)
                return redirect('add_unidade')
            except:
                messages.error(request, msgIntegridade)
                return redirect('add_unidade')
        
    context = {
        'form': form,
        'form_dep': form_dep,
        'form_divis': form_divis,
    }

    return render(request, template_name, context)

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
                messages.success(request, msgSucesso)
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

    objs_tipo = MaterialTipo.objects.prefetch_related('material_obj').order_by('id')

    paginator = Paginator(objs_tipo, 13)
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
        'marca_modelo': marca_modelo,
    }

    return render(request, template_name, context)

@login_required
def itemSaidaViewLista(request):
    template_name = 'include/listar_saida.html' 

    objs = []

    objs_tipo = MaterialTipo.objects.filter(saida_obj__isnull=False).prefetch_related('material_obj').order_by('id') 

    paginator = Paginator(objs_tipo, 15)
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
def noExitItemsView(request):
    template_name = 'include/listar_dispo.html'
    
    objs = []

    objs_tipo = MaterialTipo.objects.filter(saida_obj__isnull=True).prefetch_related('material_obj').order_by('id')

    paginator = Paginator(objs_tipo, 13)
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
    template_name = 'account/hist_usuario.html'

    objs = []

    objs_tipo = HistoricoUser.objects.all().order_by('id')

    paginator = Paginator(objs_tipo, 15)
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
def filtro_view(request, id):
    form = FiltroForm(data=request.GET)

    if form.is_valid():
        unidade = form.cleaned_data['unidade']
        departamento = form.cleaned_data['departamento']
        divisao = form.cleaned_data.get('divisao')  # Pode ser None
        n_processo = form.cleaned_data['n_processo']

        saida = MaterialSaida.objects.create(
            unidade=unidade,
            departamento=departamento,
            divisao_field=divisao if divisao else None,  # Definindo None caso esteja vazio
            n_processo=n_processo
        )
        messages.success(request, "Saida de material realizada com sucesso!")

        try:
            material_tipo = get_object_or_404(MaterialTipo, id=id)
            material_tipo.saida_obj = saida
            material_tipo.save()
            return redirect('listar_items')
        except MaterialTipo.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'MaterialTipo não encontrado'}, status=404)

    context = {'form': form, 'material_tipo': None}
    return render(request, 'include/criar_saida_filtro.html', context)

class jsFiltroJson(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, _request):
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
    
class ChartDepResponse(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, _request):

        contagem_departamentos = (
            MaterialSaida.objects.values('departamento__nome')
            .annotate(total=Count('departamento'))
            .order_by('departamento__nome')
        )
        serializer = DepartamentoCountSerializer(contagem_departamentos, many=True)

        return Response({'contagem_departamentos': serializer.data})

def EstatisticasView(request):
    template_name = 'analise_dados/estatisticas.html'
    
    materialtipos = MaterialTipo.objects.filter(saida_obj__isnull=False).select_related('saida_obj__departamento', 'saida_obj__unidade')

    itens_por_unidade_departamento = defaultdict(list)
    for item in materialtipos:
        unidade_nome = item.saida_obj.unidade.unidade  
        departamento_nome = item.saida_obj.departamento.nome
        chave = ("Unidade: " + unidade_nome, "Departamento: " + departamento_nome)
        itens_por_unidade_departamento[chave].append(item)

    context = {
        'itens_por_unidade_departamento': dict(itens_por_unidade_departamento)
    }
    return render(request, template_name, context)

def MetricasView(request):
    template_name = 'analise_dados/metricas.html'
    return render(request, template_name)

def ChartsView(request):
    template_name = 'analise_dados/graficos.html'
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
    data = receber_dados_divisao(request)
    return JsonResponse(data, safe=False)

def BuscarView(request):
    template_name = 'include/buscar.html'
    form = BuscarItemForm(request.POST or None)

    items_queryset = MaterialTipo.objects.all()
    item_nome = request.POST.get('item', '')

    if form.is_valid():
        item = form.cleaned_data['item']
        if item:
            items_queryset = items_queryset.filter(modelo__icontains=item)
            if not items_queryset.exists():
                messages.error(request, 'Não consta nenhum dado com esse caracter!')

    paginator = Paginator(items_queryset, 15)
    page = request.GET.get('page')

    try:
        lista_items = paginator.page(page)
    except PageNotAnInteger:
        lista_items = paginator.page(1)
    except EmptyPage:
        lista_items = paginator.page(paginator.num_pages)

    context = {
        'form': form,
        'items': lista_items,
    }

    return render(request, template_name, context)




