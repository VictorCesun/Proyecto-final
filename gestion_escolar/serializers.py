from rest_framework import serializers
from .models import Alumno, Docente, Calificacion, Asistencia

# 📌 Serializador para Alumno
class AlumnoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alumno
        fields = '__all__'

# 📌 Serializador para Docente
class DocenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Docente
        fields = '__all__'

# 📌 Serializador para Calificación
class CalificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calificacion
        fields = '__all__'

# 📌 Serializador para Asistencia
class AsistenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asistencia
        fields = '__all__'
