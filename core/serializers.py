from rest_framework import serializers
from . models import Unidade, Departamento, Divisao

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
