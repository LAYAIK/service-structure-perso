from rest_framework import serializers
from .models import Structure, HistoriqueStructure

class StructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Structure
        fields = '__all__'
        
class HistoriqueStructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoriqueStructure
        fields = '__all__'