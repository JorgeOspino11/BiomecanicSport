"""
Vistas y Controladores REST para core_app.
Actúan como adaptadores HTTP del patrón MVC, delegando la lógica a AtletaService.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from .serializers import AtletaSerializer
from .services import AtletaService


class AtletaListCreateView(APIView):
    """
    Controlador para listar y registrar perfiles de atletas.
    Delega las operaciones de negocio a AtletaService.
    """

    def get(self, request):
        """Lista todos los atletas registrados."""
        atletas = AtletaService.listar_todos()
        serializer = AtletaSerializer(atletas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Crea un nuevo atleta validando la solicitud y delegando a AtletaService.
        """
        serializer = AtletaSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"errores_validacion": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Delegación a la capa de servicios (Service Layer)
            nuevo_atleta = AtletaService.crear_perfil(serializer.validated_data)
            resultado = AtletaSerializer(nuevo_atleta)
            return Response(
                {
                    "mensaje": "Perfil de atleta registrado exitosamente.",
                    "atleta": resultado.data
                },
                status=status.HTTP_201_CREATED
            )
        except ValidationError as error:
            return Response(
                {"error_negocio": str(error)},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        except Exception as error:
            return Response(
                {"error_interno": f"Ocurrió un error inesperado: {str(error)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AtletaDetailView(APIView):
    """
    Controlador para consultar el detalle de un atleta específico.
    """

    def get(self, request, pk):
        try:
            atleta = AtletaService.obtener_por_id(pk)
            serializer = AtletaSerializer(atleta)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(
                {"error": f"No se encontró un atleta con ID {pk}."},
                status=status.HTTP_404_NOT_FOUND
            )
