from django.contrib import admin
from .models import Categoria, Producto, Cliente, Trekking, Comments

admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(Cliente)


if not admin.site.is_registered(Trekking):
    admin.site.register(Trekking)

if not admin.site.is_registered(Comments):
    admin.site.register(Comments)