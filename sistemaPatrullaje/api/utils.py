from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from .models import Usuario
from math import sqrt

def obtener_usuario_desde_token(request):
    auth = request.headers.get("Authorization")

    if not auth or not auth.startswith("Bearer "):
        return None

    token = auth.split(" ")[1]

    try:
        decoded = AccessToken(token)
        usuario_id = decoded["usuario_id"]
        return Usuario.objects.get(id=usuario_id)
    except:
        return None

def calcular_distancia(lat1, lon1, lat2, lon2):
    # distancia simple
    return sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)




