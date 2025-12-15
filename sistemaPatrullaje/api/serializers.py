from rest_framework import serializers
from .models import PersonalExterno, Rol, Usuario, RegistroPatrulla

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = "__all__"


class PersonalExternoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalExterno
        fields = "__all__"


class UsuarioSerializer(serializers.ModelSerializer):
    personal_externo = PersonalExternoSerializer(read_only=True)
    rol = RolSerializer(read_only=True)

    class Meta:
        model = Usuario
        fields = "__all__"


class RegistroUsuarioSerializer(serializers.Serializer):
    dni = serializers.CharField()
    contraseña = serializers.CharField(write_only=True)
    rol = serializers.PrimaryKeyRelatedField(queryset=Rol.objects.all())

    def validate(self, data):
        dni = data["dni"]

        # Verificar que existe en PersonalExterno
        try:
            personal = PersonalExterno.objects.get(dni=dni)
        except PersonalExterno.DoesNotExist:
            raise serializers.ValidationError("El DNI no está registrado.")

        # Verificar que no tenga ya usuario
        if Usuario.objects.filter(personal_externo=personal).exists():
            raise serializers.ValidationError("Este usuario ya tiene cuenta creada.")

        return data

    def create(self, validated_data):
        personal = PersonalExterno.objects.get(dni=validated_data["dni"])

        usuario = Usuario.objects.create(
            personal_externo=personal,
            rol=validated_data["rol"],
            contraseña=validated_data["contraseña"],
        )
        return usuario


class LoginSerializer(serializers.Serializer):
    dni = serializers.CharField()
    contraseña = serializers.CharField()


class RegistroPatrullaCreateSerializer(serializers.Serializer):
    id_puesto = serializers.IntegerField()
    latitud = serializers.FloatField()
    longitud = serializers.FloatField()
    cargo_operacional = serializers.CharField()
    novedad = serializers.CharField(allow_blank=True)


class DashboardRegistroSerializer(serializers.ModelSerializer):
    apellido = serializers.CharField(
        source="patrulla.usuario.personal_externo.apellido"
    )
    nombre = serializers.CharField(
        source="patrulla.usuario.personal_externo.nombre"
    )
    grado = serializers.CharField(
        source="patrulla.usuario.personal_externo.grado"
    )
    puesto = serializers.CharField(
        source="puesto.nombre"
    )

    class Meta:
        model = RegistroPatrulla
        fields = [
            "apellido",
            "nombre",
            "grado",
            "puesto",
            "cargo_operacional",
            "fecha_hora_registro",
            "latitud_escaneo",
            "longitud_escaneo",
            "distancia_validada",
            "estado_validacion",
        ]

