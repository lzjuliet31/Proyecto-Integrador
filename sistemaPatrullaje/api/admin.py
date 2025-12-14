from django.contrib import admin
from .models import PersonalExterno, Rol, Usuario, Puesto, Patrulla, RegistroPatrulla
# Register your models here.
admin.site.register(PersonalExterno)
admin.site.register(Rol)
admin.site.register(Usuario)
admin.site.register(Puesto)
admin.site.register(Patrulla)
admin.site.register(RegistroPatrulla)

