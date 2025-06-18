from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.forms import inlineformset_factory
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse, HttpResponse
from django.db import IntegrityError
from django.db.models import Count
from collections import defaultdict
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
import json
import pandas as pd
import io
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

    # depts = Departamento.objects.all()

    # list_dep = []

    # for i in depts:
    #     list_dep.append({ "departamento": i.nome, "unidade": i.unidade, "unidade_id": i.unidade_id })

    # print(list_dep)
    
    return render(request, template_name)

def logoutView(request):
    auth_logout(request)
    return redirect('login_page')

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
                return redirect('listar_all')
            else:
                messages.error(request, "Erro ao salvar os itens")
        else:
            formset = TipoMaterFormset(request.POST)
            messages.error(request, "Erro ao salvar o formulário principal.")

        context = {
            'form': form,
            'formset': formset,
        }
        return render(request, template_name, context)

@login_required
def listarAllItemsView(request):
    template_name = 'include/all_items_disp.html'

    objs = MaterialTipo.objects.values('modelo').annotate(total=Count('*')).order_by('-total')

    return render(request, template_name, {'objs': objs})

def viewAllItens(request, item):
    template_name = 'include/view_itens.html'

    itens = MaterialTipo.objects.filter(modelo=item)

    objs = []

    paginator = Paginator(itens, 30)
    page = request.GET.get('page')

    try:
        objs = paginator.page(page)
    except PageNotAnInteger:
        objs = paginator.page(1)
    except EmptyPage:
        objs = paginator.page(paginator.num_pages)

    context = {
        'itens': itens,
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
            return redirect('listar_all')
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
            HistoricoUser.objects.create(
                nome_user = request.user.first_name,
                acao_realizada = 'Adição de contrato'
            )
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
        return redirect('all_disponiveis')

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
            )
            messages.success(request, "Atualizado com sucesso!")
            return redirect('listar_all')  
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
            return redirect('listar_all')
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

    paginator = Paginator(objs_tipo, 30)
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
            return redirect('all_disponiveis')
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

        objs = MaterialSaida.objects.values('unidade__unidade', 'departamento__nome').annotate(total=Count('*')).order_by('-total')
        objs = objs[:8]

        items_ajust = []

        for i in objs:
            items_ajust.append({ "Unidade": i['unidade__unidade'], "Departamento": i['departamento__nome'], "Total": i['total'] })
            
        serializer_saida = MaterialSaidaSerializer(items_ajust, many=True)
        # serializer_objs = MaterialTipoSerializer(items, many=True)

        return Response({'items_saida': serializer_saida.data})
    
@csrf_exempt
def relatorioResponse(request):

    if request.method == 'POST':
        try: 
            data = json.loads(request.body)
            mensagem = data.get('mensagem', '')

            return JsonResponse({'status': 'ok', 'mensagem_recebida': mensagem})
        except Exception as e:
            return JsonResponse({'status': 'erro', 'erro': str(e)}, status=400)
    else:
        return JsonResponse({'status': 'erro', 'mensagem': 'Método não permitido'}, status=405)

def MetricasView(request):
    template_name = 'analise_dados/metricas.html'

    dados = get_estat_divisoes(request)

    if request.method == 'POST':
        try:
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
                    unidade = saida.split('-')[1] if saida else "Não atrelado"
                    linhas.append({
                        "Departamento": departamento,
                        "Unidade": unidade,
                        "Marca": item["Marca"],
                        "Modelo": item["Modelo"],
                        "Número de série": item["Número de série"],
                        "Patrimonio": item["Patrimonio"],
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
            response['Content-Disposition'] = 'attachment; filename="itens_individuais.xlsx"'
            return response
        except Exception as e:
            messages.error(request, f"Ocorreu um erro: {e}")
            return redirect('metricas_page')
        
    context = {
        'dados': dados,
    }

    return render(request, template_name, context)

def count_dep(request, dep, uni, dep_nome):
    template_name = 'include/count_dep.html'

    #I have all of the elements in one query when i use select related
    itens = MaterialTipo.objects.select_related(
        'saida_obj', 
        'saida_obj__unidade', 
        'saida_obj__departamento', 
        'saida_obj__divisao_field'
        ).filter(
            saida_obj__departamento_id=dep, 
            saida_obj__unidade_id=uni)

    return render(request, template_name, {'itens': itens, 'dep_nome': dep_nome})

def RetornarExcell(request):
        
    if request.method == 'POST':
        try:
            objs = MaterialTipo.objects.values(
                'marca',
                'modelo',
                'saida_obj__departamento__nome',
                'saida_obj__unidade__unidade'
            ).annotate(total=Count('*')).exclude(saida_obj=None)

            items = []
            for i in objs:
                items.append({
                    "Marca": i['marca'],
                    "Modelo": i['modelo'],
                    "Departamento": i['saida_obj__departamento__nome'],
                    "Unidade": i['saida_obj__unidade__unidade'],
                    "Total": i['total']
                })

            df = pd.DataFrame(items)

            df_grouped = df.groupby(
                ['Departamento', 'Unidade', 'Marca', 'Modelo'],
                as_index=False
            ).agg({'Total': 'sum'})

            df_grouped = df_grouped.sort_values(['Departamento', 'Unidade', 'Marca', 'Modelo'])

            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                df_grouped.to_excel(writer, index=False, sheet_name='Itens')

            buffer.seek(0)
            response = HttpResponse(
                buffer,
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = 'attachment; filename="itens_agrupados.xlsx"'
            return response
        except Exception as e:
            messages.error(request, f"Ocorreu um erro: {e}")
            return redirect('metricas_page')

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

    paginator = Paginator(items_queryset, 20)
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

#Em alteração !
def UnidadeAddView(request):
    template_name = 'include/unidade_add.html'
    form = AddUnidadeForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            try:
                form.save()
                messages.success(request, msgSucesso)
                return redirect('unidade_add')
            except IntegrityError:
                messages.error(request, msgIntegridade)
                return redirect('unidade_add')
            except Exception as e:
                messages.error(request, f"Ocorreu um erro: {e}")
                return redirect('unidade_add')

    objs = []

    objs_unid = Unidade.objects.all()

    paginator = Paginator(objs_unid, 5)
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
        'form': form,
        'objs': objs
    }

    return render(request, template_name, context)

def DepartamentoAddView(request):
    template_name = 'include/depar_add.html'
    form = AddDepartForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            try:
                form.save()
                messages.success(request, msgSucesso)
                return redirect('depart_add')
            except IntegrityError:
                messages.error(request, msgIntegridade)
                return redirect('depart_add')  
            except Exception as e:
                messages.error(request, f"Ocorreu um erro: {e}")
                return redirect('depart_add')       
            
    objs = []
    # Use select_related to fetch related Unidade objects in the same query
    objs_dep = Departamento.objects.select_related('unidade').all()

    paginator = Paginator(objs_dep, 5)
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
        'form': form,
        'objs': objs,
    }

    return render(request, template_name, context)

def DivisaoAddView(request):
    templaete_name = 'include/divisao_add.html'
    form = AddDivisaoForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            try:
                form.save()
                messages.success(request, msgSucesso)
                return redirect('divisao_add')
            except IntegrityError:
                messages.error(request, msgIntegridade)
                return redirect('divisao_add')
            except Exception as e:
                messages.error(request, f"Ocorreu um erro: {e}")
                return redirect('divisao_add')

    objs = []
    # Use select_related to fetch related Unidade objects in the same query
    objs_div = Divisao.objects.select_related('departamento').all()

    paginator = Paginator(objs_div, 5)
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
        'form': form,
        'objs': objs,
    }

    return render(request, templaete_name, context)

def BuscarNserieView(request):
    template_name = 'include/buscar_serie.html'

    obj = None
    n_serie = None

    if request.method == 'POST':
        n_serie = request.POST.get('n_serie')

        try:
            obj = MaterialTipo.objects.filter(n_serie=n_serie)
        except MaterialTipo.DoesNotExist:
            messages.error(request, msgIntegridade)
            return render('buscar_nserie')

    context = {
        'obj': obj,
        'n_serie': n_serie,
    }

    return render(request, template_name, context)

def BuscarPatrimonioView(request):
    template_name = 'include/buscar_patrim.html'

    obj = None
    patrimonio = None

    if request.method == 'POST':
        patrimonio = request.POST.get('patrimonio')

        try:
            obj = MaterialTipo.objects.filter(patrimonio=patrimonio)
        except MaterialTipo.DoesNotExist:
            messages.error(request, msgIntegridade)
            return render('buscar_nserie')

    context = {
        'obj': obj,
        'patrimonio': patrimonio,
    }

    return render(request, template_name, context)

def all_disponiveis(request):
    template_name = 'include/all_no_exit.html'

    objs = MaterialTipo.objects.values('modelo').annotate(total=Count('*')).filter(saida_obj__isnull=True)

    return render(request, template_name, {'objs': objs})

def all_disponiveisView(request, item):
    template_name = 'include/no_exit_view.html'

    itens = MaterialTipo.objects.filter(modelo=item, saida_obj__isnull=True)

    objs = []

    paginator = Paginator(itens, 30)
    page = request.GET.get('page')

    try:
        objs = paginator.page(page)
    except PageNotAnInteger:
        objs = paginator.page(1)
    except EmptyPage:
        objs = paginator.page(paginator.num_pages)

    context = {
        'itens': itens,
        'objs': objs,
    }

    return render(request, template_name, context)

def all_ItensExit(request):
    template_name = 'include/all_exit_itens.html'

    objs = MaterialTipo.objects.values('modelo').annotate(total=Count('*')).filter(saida_obj__isnull=False)

    return render(request, template_name, {'objs': objs})

def all_saidaExitView(request, item):
    template_name = 'include/exit_view.html'

    itens = MaterialTipo.objects.filter(modelo=item, saida_obj__isnull=False)
    
    objs = []

    paginator = Paginator(itens, 30)
    page = request.GET.get('page')

    try:
        objs = paginator.page(page)
    except PageNotAnInteger:
        objs = paginator.page(1)
    except EmptyPage:
        objs = paginator.page(paginator.num_pages)

    context = {
        'itens': itens,
        'objs': objs,
    }

    return render(request, template_name, context)


