# gestion_escolar/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.utils import timezone  # Si quieres usar fechas actuales
from rest_framework import viewsets  # Para los ModelViewSet de la API
from datetime import datetime  # <-- Agrega esto
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Importa tus modelos
from .models import (
    Alumno,
    Docente,
    Materia,
    Asistencia,
    Calificacion
)

# Importa tus formularios (ajusta si tienes otros)
from .forms import (
    RegistroForm,
    AlumnoForm,
    AsistenciaForm,
    DocenteForm,
    MateriaForm,
    CalificacionForm
)

# Importa tus serializers (para la API) si los usas
from .serializers import (
    AlumnoSerializer,
    CalificacionSerializer,
    DocenteSerializer,
    AsistenciaSerializer
)


# -----------------------------------------------------------------------------
# VISTA DE REGISTRO DE USUARIOS
def registro_usuario(request):
    """
    Crea un nuevo usuario Django y, dependiendo del rol,
    crea también un Alumno o un Docente asociado.
    """
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            nuevo_usuario = form.save()
            rol_elegido = form.cleaned_data.get('rol')
            if rol_elegido == 'Alumno':
                Alumno.objects.create(usuario=nuevo_usuario)
            elif rol_elegido == 'Docente':
                Docente.objects.create(usuario=nuevo_usuario)
            messages.success(request, "Tu cuenta ha sido creada exitosamente. Ahora puedes iniciar sesión.")
            return redirect('login')
    else:
        form = RegistroForm()
    return render(request, "tu_app/registro.html", {"form": form})


# -----------------------------------------------------------------------------
# VISTAS PARA ALUMNOS
def lista_alumnos(request):
    """Muestra una lista de todos los Alumnos."""
    alumnos = Alumno.objects.all()
    return render(request, 'gestion/lista_alumnos.html', {'alumnos': alumnos})


def crear_alumno(request):
    """Crea un nuevo Alumno usando AlumnoForm."""
    if request.method == 'POST':
        form = AlumnoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_alumnos')
    else:
        form = AlumnoForm()
    return render(request, 'gestion/from_alumno.html', {'form': form})


# -----------------------------------------------------------------------------
# VISTAS PARA ASISTENCIA (MÉTODO TRADICIONAL)
def registrar_asistencia(request):
    """Crea un registro de Asistencia individual usando AsistenciaForm."""
    if request.method == 'POST':
        form = AsistenciaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ver_asistencia')
    else:
        form = AsistenciaForm()
    return render(request, 'gestion/registrar_asistencia.html', {'form': form})


def ver_asistencia(request):
    query = request.GET.get('q', '')
    if query:
        asistencias = Asistencia.objects.filter(
            Q(alumno__nombre__icontains=query) |
            Q(alumno__apellido__icontains=query)
        ).order_by('-fecha')
    else:
        asistencias = Asistencia.objects.all().order_by('-fecha')
    context = {
        'asistencias': asistencias,
        'query': query,  # para rellenar el input de búsqueda
    }
    return render(request, 'gestion/ver_asistencia.html', context)

def tomar_asistencia(request):
    alumnos = Alumno.objects.all()
    materias = Materia.objects.all()

    if request.method == 'POST':
        materia_id = request.POST.get('materia')
        fecha_str = request.POST.get('fecha')

        if not materia_id or not fecha_str:
            messages.error(request, "Debe seleccionar la materia y la fecha.")
            return redirect('tomar_asistencia')

        # Convertimos a objeto Materia
        try:
            materia_seleccionada = Materia.objects.get(pk=materia_id)
        except Materia.DoesNotExist:
            messages.error(request, "La materia seleccionada no existe.")
            return redirect('tomar_asistencia')

        # Convertimos el texto de fecha a date
        fecha_date = datetime.strptime(fecha_str, '%Y-%m-%d').date()

        # Para cada alumno, creamos un Asistencia con el estado escogido
        for alumno in alumnos:
            # name="estado_{alumno.id}" en el form
            estado_name = f'estado_{alumno.id}'
            estado_value = request.POST.get(estado_name, 'P')  # 'P' por defecto

            Asistencia.objects.create(
                alumno=alumno,
                materia=materia_seleccionada,
                fecha=fecha_date,
                estado=estado_value
            )

        messages.success(request, "¡Asistencia guardada correctamente!")
        return redirect('ver_asistencia')
    else:
        # GET: Mostrar formulario
        contexto = {
            'alumnos': alumnos,
            'materias': materias,
            'fecha_hoy': timezone.now().date(),
        }
        return render(request, 'gestion/tomar_asistencia.html', contexto)
# -----------------------------------------------------------------------------
# VISTA DE LOGIN PERSONALIZADO
class LoginViewPorRol(LoginView):
    template_name = "tu_app/login.html"

    def get_success_url(self):
        user = self.request.user

        # Si el usuario tiene perfil Docente
        if hasattr(user, 'docente') and user.docente is not None:
            # Redirige a "tomar_asistencia" 
            return reverse_lazy('tomar_asistencia')

        # Si el usuario tiene perfil Alumno
        elif hasattr(user, 'alumno') and user.alumno is not None:
            return reverse_lazy('ver_asistencia')

        # En caso de no tener perfil de alumno ni docente, lo mandamos a 'home'
        return reverse_lazy('home')


#-----------------------------------------------------------------------------
# Ca
@login_required
def registrar_calificacion(request):
    try:
        docente = Docente.objects.get(usuario=request.user)
    except Docente.DoesNotExist:
        messages.error(request, "Tu usuario no está registrado como docente.")
        return redirect('home')

    materias = Materia.objects.filter(docente=docente)
    materia_id = request.GET.get('materia')
    materia_seleccionada = None
    registros = []

    if materia_id:
        materia_seleccionada = get_object_or_404(Materia, id=materia_id, docente=docente)
        alumnos = Alumno.objects.all().order_by('apellido', 'nombre')

        if request.method == 'GET':
            registros = Calificacion.objects.filter(
                materia=materia_seleccionada,
                docente=docente
            ).select_related('alumno').order_by('alumno__apellido', 'alumno__nombre')

        elif request.method == 'POST':
            for alumno in alumnos:
                calificacion, _ = Calificacion.objects.get_or_create(
                    alumno=alumno,
                    materia=materia_seleccionada,
                    docente=docente,
                    defaults={'calificacion': 0}
                )

                field_name = f'calificacion_{calificacion.id}'
                nueva_calificacion = request.POST.get(field_name)

                if nueva_calificacion is not None and nueva_calificacion.strip() != "":
                    try:
                        calificacion.calificacion = float(nueva_calificacion)
                        calificacion.save()
                    except ValueError:
                        messages.warning(request, f"Valor inválido para {alumno}")
                else:
                    messages.warning(request, f"No se proporcionó calificación para {alumno}")

                registros.append(calificacion)

            registros.sort(key=lambda r: (r.alumno.apellido.lower(), r.alumno.nombre.lower()))
            messages.success(request, "Calificaciones actualizadas correctamente.")
            return redirect(f'{reverse("registrar_calificacion")}?materia={materia_id}')

    context = {
        'materias': materias,
        'registros': registros,
        'materia_id': materia_id,
        'materia_seleccionada': materia_seleccionada,
    }
    return render(request, 'gestion/registrar_calificacion.html', context)


# -----------------------------------------------------------------------------
# VIEWSETS PARA LA API (DRF)
class AlumnoViewSet(viewsets.ModelViewSet):
    queryset = Alumno.objects.all()
    serializer_class = AlumnoSerializer

class CalificacionViewSet(viewsets.ModelViewSet):
    queryset = Calificacion.objects.all()
    serializer_class = CalificacionSerializer

class DocenteViewSet(viewsets.ModelViewSet):
    queryset = Docente.objects.all()
    serializer_class = DocenteSerializer

class AsistenciaViewSet(viewsets.ModelViewSet):
    queryset = Asistencia.objects.all()
    serializer_class = AsistenciaSerializer

@login_required
def lista_calificaciones(request):
    calificaciones = Calificacion.objects.all()
    return render(request, "gestion/lista_calificaciones.html", {"calificaciones": calificaciones})

