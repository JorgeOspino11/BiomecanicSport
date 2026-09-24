"""
Serializadores de Django REST Framework para la entidad Atleta.
"""
from rest_framework import serializers
from .models import Atleta


class AtletaSerializer(serializers.ModelSerializer):
    """Serializador para entrada y salida de datos del atleta."""
    
    indice_masa_corporal = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Atleta
        fields = [
            'id',
            'nombre',
            'apellido',
            'edad',
            'fecha_nacimiento',
            'peso_kg',
            'altura_cm',
            'deporte',
            'posicion_rol',
            'dominancia',
            'lesiones_previas',
            'indice_masa_corporal',
            'creado_en',
            'actualizado_en'
        ]
        read_only_fields = ['id', 'creado_en', 'actualizado_en']

    def get_indice_masa_corporal(self, obj):
        """Calcula el IMC referencial (peso / altura_en_metros^2)."""
        if obj.altura_cm and obj.peso_kg and obj.altura_cm > 0:
            altura_m = float(obj.altura_cm) / 100.0
            return round(float(obj.peso_kg) / (altura_m ** 2), 2)
        return None
