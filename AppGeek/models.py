from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class Categoria(models.Model):
    nombre = models.CharField(max_length=50)


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    imagen = models.ImageField(upload_to='producto_imagenes/', blank=True, null=True)


class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    direccion = models.CharField(max_length=255, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)


class Trekking(models.Model):
    ESTADO_CHOICES = [
        ('Abierto', 'Abierto'),
        ('En Curso', 'En Curso'),
        ('Cerrado', 'Cerrado'),
    ]

    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    duracion_dias = models.IntegerField(blank=True, null=True)
    dificultad = models.CharField(max_length=20,
                                  choices=[('Fácil', 'Fácil'), ('Intermedio', 'Intermedio'), ('Difícil', 'Difícil')],
                                  default='Fácil', null=True)
    requisitos = models.TextField(blank=True, null=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='abierto')
    fecha_cierre = models.DateField(blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.estado == 'cerrado' and not self.fecha_cierre:
            self.fecha_cierre = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.nombre)


def comment_image_path(instance, filename):
    return f'comment_images/{instance.trekking.id}/{filename}'


class Comments(models.Model):
    ESTADO_CHOICES = (
        ('Abierto', 'Abierto'),
        ('Cerrado', 'Cerrado'),
        ('En Curso', 'En Curso'),
    )

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    trekking = models.ForeignKey(Trekking, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    imagen = models.ImageField(upload_to='comentario_imagenes/', blank=True, null=True)
    estado = models.CharField(max_length=50, choices=ESTADO_CHOICES, default='Abierto')
    last_updated = models.DateTimeField(auto_now=True)

# Create your models here.
