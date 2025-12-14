# api/models.py
from django.db import models

class Rol(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class PersonalExterno(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.CharField(max_length=20, unique=True)
    grado = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.grado} {self.apellido}, {self.nombre} ({self.dni})"


class Usuario(models.Model):
    personal_externo = models.OneToOneField(PersonalExterno, on_delete=models.CASCADE)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    contraseña = models.CharField(max_length=255)
    activo = models.BooleanField(default=True)

    @property
    def is_active(self):
        # SimpleJWT mira este atributo
        return self.activo

    def __str__(self):
        return f"{self.personal_externo.apellido}, {self.personal_externo.nombre}"


class Puesto(models.Model):
    nombre = models.CharField(max_length=100)
    latitud = models.FloatField()
    longitud = models.FloatField()

    def __str__(self):
        return self.nombre


class Patrulla(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha = models.DateField()

    def __str__(self):
        return f"Patrulla de {self.usuario} - {self.fecha}"


class RegistroPatrulla(models.Model):
    patrulla = models.ForeignKey(Patrulla, on_delete=models.CASCADE)
    puesto = models.ForeignKey(Puesto, on_delete=models.CASCADE)

    fecha_hora_registro = models.DateTimeField(auto_now_add=True)

    latitud_escaneo = models.FloatField()
    longitud_escaneo = models.FloatField()

    cargo_operacional = models.CharField(max_length=50)
    novedad = models.TextField(blank=True)

    distancia_validada = models.FloatField()
    estado_validacion = models.CharField(max_length=20)
