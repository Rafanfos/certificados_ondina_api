import csv
import os
from io import StringIO
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import HttpResponse, JsonResponse
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from django.utils import timezone
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from students.models import Diploma, Highlight_Certificate, Student
from reportlab.pdfbase.pdfmetrics import stringWidth


@csrf_exempt
@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def register_students(request):
    if request.method == "POST":
        try:
            # Obtenha o arquivo CSV enviado
            csv_file = request.FILES["file"]

            # Leia o conteúdo do arquivo CSV
            io_string = csv_file.read().decode("utf-8")
            reader = csv.DictReader(
                io_string.splitlines(), delimiter=","
            )  # Use splitlines para dividir em linhas

            # Itere sobre as linhas do CSV e crie os registros no banco de dados
            for row in reader:
                full_name = row[
                    "Nome Completo"
                ]  # Verifique se o cabeçalho está correto
                graduation_term = row["Trimestre"]

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
def generate_pdf(request):
    data = request.data
    director = data.get("director")
    vice_director = data.get("vice_director")
    year = data.get("year")
    student_id = data.get("student_id")
    certificate_type = data.get("certificate_type")

    try:
        if (
            certificate_type != "highlight_certificate"
            and certificate_type != "diploma"
        ):
            return JsonResponse({"error": "Invalid certificate type"}, status=400)

        student = Student.objects.get(id=student_id)
        full_name = student.full_name
        graduation_term = student.graduation_term

        # Criar o PDF
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = (
            f'attachment; filename="{full_name}_destaque.pdf"'
        )

        # Usar paisagem
        p = canvas.Canvas(response, pagesize=landscape(letter))
        width, height = landscape(letter)

        image_path = ""

        # Adicionar imagem de fundo
        if certificate_type == "highlight_certificate":
            image_path = os.path.join(
                settings.BASE_DIR, "static", "images", "highlight-model.png"
            )
        elif certificate_type == "diploma":
            image_path = os.path.join(
                settings.BASE_DIR, "static", "images", "diploma-model.png"
            )

        p.drawImage(image_path, 0, 0, width=width, height=height)

        # Adicionar uma fonte personalizada
        font_path = os.path.join(
            settings.BASE_DIR, "static", "fonts", "GreatVibes-Regular.ttf"
        )
        pdfmetrics.registerFont(TTFont("GreatVibes", font_path))

        font_size = 36
        p.setFont("GreatVibes", font_size)
        max_width = 600
        students_name_y = certificate_type == "highlight_certificate" and 370 or 300

        text_width = stringWidth(full_name, "GreatVibes", font_size)
        if text_width > max_width:
            # Divida o texto em várias linhas
            students_name_y = certificate_type == "highlight_certificate" and 310 or 240
            lines = split_text_into_lines(full_name, "GreatVibes", font_size, max_width)
            y_offset = students_name_y + (len(lines) - 1) * font_size
            for line in lines:
                p.drawCentredString(width / 2, height - y_offset, line)
                y_offset += font_size
        else:
            p.drawCentredString(width / 2, height - students_name_y, full_name)

        # Adicionar conteúdo ao PDF
        # p.drawCentredString(width / 2, height - students_name_y, f"{full_name}")

        # Desenhar caixas e adicionar texto
        box_width = 200
        box_height = 20
        box_x_start = certificate_type == "highlight_certificate" and 90 or 300
        box_y = (
            certificate_type == "highlight_certificate" and height - 530 or height - 500
        )

        # Caixa para o diretor
        font_path = os.path.join(
            settings.BASE_DIR, "static", "fonts", "CormorantGaramond-Medium.ttf"
        )

        pdfmetrics.registerFont(TTFont("CormorantGaramond-Medium", font_path))
        p.setFont("CormorantGaramond-Medium", 16)
        p.setStrokeColor("transparent")
        p.rect(box_x_start, box_y, box_width, box_height)
        p.drawCentredString(
            box_x_start + box_width / 2, box_y + box_height / 2, director
        )

        if certificate_type == "highlight_certificate":
            # Caixa para o vice-diretor
            box_x_start = 510
            p.rect(box_x_start, box_y, box_width, box_height)
            p.drawCentredString(
                box_x_start + box_width / 2, box_y + box_height / 2, vice_director
            )

            # Data e local
            font_path = os.path.join(
                settings.BASE_DIR, "static", "fonts", "Alice-Regular.ttf"
            )
            pdfmetrics.registerFont(TTFont("Alice", font_path))
            p.setFont("Alice", 17)
            p.drawCentredString(
                width / 2,
                height - 600,
                f"Belo Horizonte, {graduation_term}º Trimestre/{year}",
            )

        p.showPage()
        p.save()

        if certificate_type == "highlight_certificate":
            Highlight_Certificate.objects.update_or_create(
                student=student,
                defaults={
                    "director_name": director,
                    "vice_director_name": vice_director,
                },
            )

            student.highlight_certificate_generated = True
            student.save()
        elif certificate_type == "diploma":
            Diploma.objects.update_or_create(
                student=student,
                defaults={
                    "director_name": director,
                },
            )

            student.diploma_generated = True
            student.save()

        return response
    except Student.DoesNotExist:
        return JsonResponse({"error": "Student not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_all_students(request):

    students = Student.objects.all()

    students_data = [
        {
            "id": student.id,
            "full_name": student.full_name,
            "graduation_term": student.graduation_term,
            "diploma_generated": student.diploma_generated,
            "highlight_certificate_generated": student.highlight_certificate_generated,
        }
        for student in students
    ]

    return JsonResponse({"students": students_data}, status=200, safe=False)


def split_text_into_lines(text, font_name, font_size, max_width):
    """Quebra o texto em linhas para caber dentro da largura máxima."""
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        # Verifique a largura da linha atual com a próxima palavra
        test_line = f"{current_line} {word}".strip()
        if stringWidth(test_line, font_name, font_size) <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)

    return lines
