import csv
from io import StringIO
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Student  # Certifique-se de que o modelo está importado corretamente

@csrf_exempt
@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def register_students(request):
    if request.method == "POST":
        try:
            # Obtenha o conteúdo do arquivo CSV enviado como string
            csv_content = request.data["file"]

            # Use StringIO para tratar o conteúdo da string como se fosse um arquivo
            io_string = StringIO(csv_content)
            reader = csv.DictReader(io_string, delimiter=",")  # Delimitador padrão é ','

            # Itere sobre as linhas do CSV e crie os registros no banco de dados
            for row in reader:
                full_name = row["nome completo"]
                graduation_term = row["trimestre"]

                # Crie o registro no banco de dados
                Student.objects.create(
                    full_name=full_name,
                    graduation_term=int(graduation_term)
                )

            # Retorna sucesso se todos os alunos forem cadastrados
            return JsonResponse(
                {"message": "Students registered successfully"}, status=201
            )

        except Exception as e:
            # Captura e retorna qualquer erro ocorrido
            return JsonResponse({"error": str(e)}, status=400)

    # Método não permitido se não for POST
    return JsonResponse({"error": "Invalid request method"}, status=405)
