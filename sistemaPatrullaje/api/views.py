from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import AuthenticationFailed
#from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from datetime import date, timedelta, datetime
import jwt


from .models import Rol, Usuario, PersonalExterno, Puesto, Patrulla, RegistroPatrulla
from .serializers import (
    RolSerializer,
    UsuarioSerializer,
    PersonalExternoSerializer,
    RegistroUsuarioSerializer,
    LoginSerializer,
    RegistroPatrullaCreateSerializer,
)
from .utils import calcular_distancia, obtener_usuario_desde_token
#from .permissions import EsOperativo   # puedes usar EsSupervisor en otros endpoints


# --- LISTADOS -----------------------------------------------------------

class RolListView(APIView):
    def get(self, request):
        roles = Rol.objects.all()
        serializer = RolSerializer(roles, many=True)
        return Response(serializer.data)


class UsuarioListView(APIView):
    def get(self, request):
        usuarios = Usuario.objects.all()
        serializer = UsuarioSerializer(usuarios, many=True)
        return Response(serializer.data)


class PersonalExternoListView(APIView):
    def get(self, request):
        personas = PersonalExterno.objects.all()
        serializer = PersonalExternoSerializer(personas, many=True)
        return Response(serializer.data)


# --- REGISTRO DE USUARIO -----------------------------------------------

class RegistroUsuarioView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistroUsuarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"mensaje": "Usuario creado correctamente"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# --- LOGIN --------------------------------------------------------------

class LoginDNIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        dni = request.data.get("dni")
        contraseña = request.data.get("contraseña")

        try:
            personal = PersonalExterno.objects.get(dni=dni)
            usuario = Usuario.objects.get(personal_externo=personal)
        except:
            return Response({"error": "Credenciales inválidas"}, status=400)

        if usuario.contraseña != contraseña:
            return Response({"error": "Credenciales inválidas"}, status=400)

        payload = {
            "usuario_id": usuario.id,
            "rol": usuario.rol.nombre,
            "exp": datetime.utcnow() + timedelta(hours=10),
            "iat": datetime.utcnow(),
        }

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

        return Response({
            "access": token,
            "rol": usuario.rol.nombre
        })



# --- REGISTRAR PATRULLA -------------------------------------------------

class RegistrarPatrullaView(APIView):
    
    def post(self, request):

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            raise AuthenticationFailed("Token requerido")

        try:
            token = auth_header.split(" ")[1]
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            usuario = Usuario.objects.get(id=payload["usuario_id"], activo=True)
        except:
            raise AuthenticationFailed("Token inválido")
        
         #PERMISO POR ROL
        if usuario.rol.nombre.lower() != "operador":
            return Response(
                {"error": "No tiene permisos para registrar patrulla"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = RegistroPatrullaCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        data = serializer.validated_data

        puesto = Puesto.objects.get(id=data["id_puesto"])

        patrulla, _ = Patrulla.objects.get_or_create(
            usuario=usuario,
            fecha=date.today()
        )

        distancia = calcular_distancia(
            data["latitud"],
            data["longitud"],
            puesto.latitud,
            puesto.longitud
        )

        estado = "VALIDO" if distancia <= 50 else "RECHAZADO"

        registro = RegistroPatrulla.objects.create(
            patrulla=patrulla,
            puesto=puesto,
            cargo_operacional=data["cargo_operacional"],
            novedad=data.get("novedad", ""),
            latitud_escaneo=data["latitud"],
            longitud_escaneo=data["longitud"],
            distancia_validada=distancia,
            estado_validacion=estado
        )

        return Response({
            "mensaje": "Registro guardado correctamente",
            "puesto": puesto.nombre,
            "distancia": distancia,
            "estado": estado
        }, status=201)
