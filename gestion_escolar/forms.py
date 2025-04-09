# gestion_escolar/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Alumno, Docente, Materia, Calificacion, Asistencia

# Opciones de rol de usuario para RegistroForm
ROL_CHOICES = [
    ('Alumno', 'Alumno'),
    ('Docente', 'Docente'),
]

class RegistroForm(UserCreationForm):
    """
    Formulario para registrar un usuario (Django User)
    con un rol seleccionado (Alumno o Docente).
    """
    rol = forms.ChoiceField(choices=ROL_CHOICES, required=True, label="Tipo de usuario")

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "rol"]
        labels = {
            'username': 'Nombre de usuario',
            'email': 'Correo electrónico',
            'password1': 'Contraseña',
            'password2': 'Confirmar contraseña',
            'rol': 'Tipo de usuario',
        }


class AlumnoForm(forms.ModelForm):
    """
    Formulario para crear/editar un Alumno.
    """
    class Meta:
        model = Alumno
        fields = ['usuario', 'matricula', 'nombre', 'apellido', 'fecha_nacimiento']


class DocenteForm(forms.ModelForm):
    """
    Formulario para crear/editar un Docente.
    """
    class Meta:
        model = Docente
        fields = ['usuario', 'nombre', 'apellido']


class MateriaForm(forms.ModelForm):
    """
    Formulario para crear/editar una Materia.
    """
    class Meta:
        model = Materia
        fields = ['nombre', 'docente']


class CalificacionForm(forms.ModelForm):
    class Meta:
        model = Calificacion
        fields = ["alumno", "materia", "calificacion", 'docente']

    def __init__(self, *args, **kwargs):
        docente = kwargs.pop("docente", None)
        super().__init__(*args, **kwargs)

        if docente:
            # Filtrar materias y alumnos que correspondan al docente
            self.fields["materia"].queryset = Materia.objects.filter(docente=docente)
            self.fields["alumno"].queryset = Alumno.objects.all()


class AsistenciaForm(forms.ModelForm):
    """
    Formulario para crear/editar Asistencia,
    usando un campo 'estado' con las opciones (Presente, Falta, Retardo).
    """
    class Meta:
        model = Asistencia
        fields = ['alumno', 'materia', 'fecha', 'estado']
        labels = {
            'alumno': 'Alumno',
            'materia': 'Materia',
            'fecha': 'Fecha',
            'estado': 'Estado',
        }
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
        }
