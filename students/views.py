import csv
from io import StringIO
import os
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Student
from django.http import HttpResponse, JsonResponse
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from django.utils import timezone
from .models import Student, HighlightCertificate
from django.contrib.staticfiles.storage import staticfiles_storage


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
            reader = csv.DictReader(
                io_string, delimiter=","
            )  # Delimitador padrão é ','

            # Itere sobre as linhas do CSV e crie os registros no banco de dados
            for row in reader:
                full_name = row["nome completo"]
                graduation_term = row["trimestre"]

                # Crie o registro no banco de dados
                Student.objects.create(
                    full_name=full_name, graduation_term=int(graduation_term)
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


@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def highlight_pdf(request):
    data = request.data
    director = data.get("director")
    vice_director = data.get("vice_director")
    student_id = data.get("student_id")  # ID do aluno em destaque

    try:
        student = Student.objects.get(id=student_id)
        full_name = student.full_name
        graduation_term = student.graduation_term
        current_year = timezone.now().year

        # Criar o PDF
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = (
            f'attachment; filename="{full_name}_destaque.pdf"'
        )

        # Usar paisagem
        p = canvas.Canvas(response, pagesize=landscape(letter))
        width, height = landscape(letter)

        # Adicionar imagem de fundo
        image_path = os.path.join(
            settings.BASE_DIR, 'static', 'images', 'highlight-model.png'
        )
        p.drawImage(image_path, 0, 0, width=width, height=height)

        # Adicionar conteúdo ao PDF
        p.setFont("Helvetica", 20)
        p.drawCentredString(width / 2, height - 350, f"{full_name}")

        # Desenhar caixas e adicionar texto
        box_width = 200
        box_height = 20
        box_x_start = 140
        box_y = height - 530

        # Caixa para o diretor
        p.setStrokeColor('transparent')
        p.setFont("Helvetica", 14)
        p.rect(box_x_start, box_y, box_width, box_height)
        p.drawCentredString(
            box_x_start + box_width / 2, box_y + box_height / 2, director
        )

        # Caixa para o vice-diretor
        box_x_start = 485
        p.rect(box_x_start, box_y, box_width, box_height)
        p.drawCentredString(
            box_x_start + box_width / 2, box_y + box_height / 2, vice_director
        )

        # Data e local
        p.setFont("Helvetica", 17)
        p.drawCentredString(
            width / 2,
            height - 600,
            f"Belo Horizonte, {graduation_term}º Trimestre /{current_year}",
        )

        p.showPage()
        p.save()

        # Criar ou atualizar o certificado
        HighlightCertificate.objects.update_or_create(student=student)

        return response
    except Student.DoesNotExist:
        return JsonResponse({"error": "Student not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
