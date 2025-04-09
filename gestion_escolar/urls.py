from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from .views import registrar_calificacion, lista_calificaciones

from .views import (
    registro_usuario,
    lista_alumnos,
    crear_alumno,
    registrar_asistencia,
    ver_asistencia,
    LoginViewPorRol,
    # Asegúrate de importar la función:
    tomar_asistencia,  
    # Los ViewSets:
    AlumnoViewSet,
    CalificacionViewSet,
    DocenteViewSet,
    AsistenciaViewSet
)


router = DefaultRouter()
router.register(r'alumnos', AlumnoViewSet)
router.register(r'docentes', DocenteViewSet)
router.register(r'calificaciones', CalificacionViewSet)
router.register(r'asistencias', AsistenciaViewSet)

urlpatterns = [
    path('', LoginViewPorRol.as_view(), name='home'),
    path('login/', LoginViewPorRol.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('registro/', registro_usuario, name='registro'),

    path('alumnos/', lista_alumnos, name='lista_alumnos'),
    path('alumnos/nuevo/', crear_alumno, name='crear_alumno'),
    path('asistencia/registrar/', registrar_asistencia, name='registrar_asistencia'),
    path('asistencia/', ver_asistencia, name='ver_asistencia'),

    # La nueva ruta para tomar asistencia
    path('asistencia/tomar/', tomar_asistencia, name='tomar_asistencia'),
    path("calificaciones/nueva/", registrar_calificacion, name="registrar_calificacion"),
    path("calificaciones/", lista_calificaciones, name="lista_calificaciones"),

    path('api/', include(router.urls)),
]

