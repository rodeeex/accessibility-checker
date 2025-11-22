import os
import tempfile
from datetime import datetime
from xhtml2pdf import pisa


def generate_pdf_report(report_data: dict) -> str:
    """
    Генерирует PDF отчет путем конвертации HTML

    :param report_data: Данные для отчета
    :return: Путь к созданному PDF файлу
    """
    from .html import generate_html_report

    html_content = generate_html_report(report_data)

    temp_dir = tempfile.gettempdir()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_filename = f"accessibility_report_{timestamp}.pdf"
    pdf_path = os.path.join(temp_dir, pdf_filename)

    # Конвертируем HTML в PDF
    with open(pdf_path, "wb") as pdf_file:
        pisa_status = pisa.CreatePDF(html_content, dest=pdf_file)

    if pisa_status.err:
        raise Exception(f"Ошибка при создании PDF: {pisa_status.err}")

    return pdf_path
