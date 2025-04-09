# gestion_escolar/models.py

from django.db import models
from django.contrib.auth.models import User

class Docente(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    # Si deseas forzar nombre/apellido, no uses blank=True ni null=True
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)

    def __str__(self):
        return f"Docente: {self.nombre} {self.apellido}"


class Alumno(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    matricula = models.CharField(max_length=20, blank=True, null=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    apellido = models.CharField(max_length=100, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)

    def __str__(self):
        if self.nombre or self.apellido:
            return f"Alumno: {self.nombre} {self.apellido}"
        return f"Alumno (usuario: {self.usuario.username})"


class Materia(models.Model):
    nombre = models.CharField(max_length=100)
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


class Asistencia(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    fecha = models.DateField()

    # Estados de asistencia
    ESTADOS = (
        ('P', 'Presente'),
        ('F', 'Falta'),
        ('R', 'Retardo'),
    )
    estado = models.CharField(
        max_length=1,
        choices=ESTADOS,
        default='P',  # Por defecto, se marca "Presente"
    )

    def __str__(self):
        return f"Asistencia de {self.alumno} a {self.materia} el {self.fecha}: {self.get_estado_display()}"


class Calificacion(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE)  # No debe ser NULL
    calificacion = models.FloatField()


    def __str__(self):
        return f"Calificación {self.calificacion} para {self.alumno} en {self.materia}"
