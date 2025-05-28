from . models import *
from collections import Counter
from collections import defaultdict
import pandas as pd
from django.http import HttpResponse
import io

def criar_pdf():
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

    return print("Sucesso!")

def receber_dados_divisao(request):
    # Dicionário para agrupar os itens por divisão
    agrupados_por_divisao = defaultdict(list)

    # Obter todos os objetos de MaterialTipo
    material_tipos = MaterialTipo.objects.select_related('saida_obj__divisao_field').all()

    for item in material_tipos:
        # Obter a divisão associada ao item
        divisao = item.saida_obj.divisao_field.nome if item.saida_obj and item.saida_obj.divisao_field else "Sem Divisão"

        # Adicionar o item ao grupo correspondente à divisão
        agrupados_por_divisao[divisao].append(item.get_complete_object())

    # Organizar os resultados em uma lista
    resultado = []
    for divisao, itens in agrupados_por_divisao.items():
        resultado.append({
            "divisao": divisao,
            "itens": itens
        })
    
    return resultado

def receber_dados_departamento(request):
    # Dicionário para agrupar os itens por divisão
    agrupados_por_divisao = defaultdict(list)

    # Obter todos os objetos de MaterialTipo
    material_tipos = MaterialTipo.objects.select_related('saida_obj__departamento').all()

    for item in material_tipos:
        # Obter o departamento associado ao item
        departamento = item.saida_obj.departamento.nome if item.saida_obj and item.saida_obj.departamento else "Sem Departamento"

        # Adicionar o item ao grupo correspondente à divisão
        agrupados_por_divisao[departamento].append(item.get_complete_object())

    # Organizar os resultados em uma lista
    resultado = []
    for departamento, itens in agrupados_por_divisao.items():
        resultado.append({
            "Departamento": departamento,
            "itens": itens
        })
    
    return resultado


def items_dados(request):
    material_tipo_saida = MaterialSaida.objects.all()
    material_tipo = MaterialTipo.objects.all()

    each_item = []

    items_iguais = Counter()

    for obj in material_tipo:
        for obj_saida in material_tipo_saida:
            if obj.id == obj_saida.id:
                each_item.append( f"[Material: {obj} Saida: {obj_saida}]")
                if obj.id and obj_saida.id:
                    items_iguais[( f"( Marca: {obj.marca} ) (Modelo: {obj_saida} )" )] += 1

    return each_item

def item_agrupados(request):
    material_tipo_saida = MaterialSaida.objects.all()
    material_tipo = MaterialTipo.objects.all()

    items_iguais = Counter()

    for obj in material_tipo:
        for obj_saida in material_tipo_saida:
            if obj.id == obj_saida.id and obj_saida.unidade:
                items_iguais[f"[Marca: {obj.marca} Modelo: {obj.modelo} Unidade: {obj_saida.unidade} Departamento: {obj_saida.departamento} Divisão: {obj_saida.divisao_field}]"] += 1

    return items_iguais

def get_estatisticas_unidades(request):
    saidas_unidades = MaterialSaida.objects.prefetch_related('unidade').all()

    dados_unidades = []

    if saidas_unidades:
        for i in saidas_unidades:
            nome_unidade = str(i.unidade).split(" ")[0]

            qnt_unidade = MaterialSaida.objects.filter(unidade=i.unidade).count()

            dados_unidades.append(f"[ Departamentos: ({nome_unidade}) Quantidade de Items: ({qnt_unidade}) ]")

    dados_unidades = list(dict.fromkeys(dados_unidades))

    return dados_unidades

def get_estatisticas_departmentos(request):
    saidas_departamentos = MaterialSaida.objects.prefetch_related('departamento').all()

    dados_departamentos = []

    if saidas_departamentos:
        for i in saidas_departamentos:
            nome_departamento = str(i.departamento)
            qnt_departamento = MaterialSaida.objects.filter(departamento=i.departamento).count()

            dados_departamentos.append(f"[ Unidades: ({nome_departamento}) Quantidade de Items: ({qnt_departamento}) ]")

    dados_departamentos = list(dict.fromkeys(dados_departamentos))

    return dados_departamentos


