from rest_framework import serializers
from . models import *

class UnidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unidade
        fields = '__all__'

class DepartamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departamento
        fields = '__all__'

class DivisaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Divisao
        fields = '__all__'

class DepartamentoCountSerializer(serializers.Serializer):
    departamento__nome = serializers.CharField()
    total = serializers.IntegerField()

class MaterialTipoSerializer(serializers.Serializer):
    class Meta:
        model = MaterialTipo
        fields = ['modelo']

class MaterialSaidaSerializer(serializers.Serializer):
    Unidade = serializers.CharField()
    Departamento = serializers.CharField()
    Total = serializers.CharField()


