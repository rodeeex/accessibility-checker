import os
import tempfile
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.colors import HexColor


def generate_pdf_report(report_data: dict) -> str:
    """
    Генерирует PDF отчет

    :param report_data: Данные для отчета
    :return: Путь к созданному PDF файлу
    """
    # Создаем временный файл для PDF
    temp_dir = tempfile.gettempdir()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_filename = f"accessibility_report_{timestamp}.pdf"
    pdf_path = os.path.join(temp_dir, pdf_filename)

    # Создаем PDF документ
    doc = SimpleDocTemplate(pdf_path, pagesize=A4, rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=18)

    # Стили для документа
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=1,  # центр
        textColor=HexColor('#007acc')
    )

    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        spaceBefore=20,
        spaceAfter=10,
        textColor=HexColor('#333333')
    )

    normal_style = styles['Normal']

    # Содержимое документа
    story = []

    # Заголовок
    story.append(Paragraph("🔍 Отчет о проверке доступности", title_style))
    story.append(Spacer(1, 20))

    # Информация о проверке
    info_data = [
        ['URL сайта:', report_data['url']],
        ['Время проверки:', _format_timestamp(report_data['timestamp'])],
        ['Всего найдено проблем:', str(report_data['total_issues'])]
    ]

    info_table = Table(info_data, colWidths=[2*inch, 4*inch])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('BACKGROUND', (1, 0), (1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    story.append(info_table)
    story.append(Spacer(1, 20))

    # Сводка по уровням
    story.append(Paragraph("Сводка по уровням критичности", heading_style))

    level_summary = _get_level_summary(report_data["issues"])
    level_data = [['Уровень', 'Количество проблем']]
    for level in ['A', 'AA', 'AAA']:
        count = level_summary.get(level, 0)
        level_data.append([level, str(count)])

    level_table = Table(level_data, colWidths=[1.5*inch, 2*inch])
    level_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#007acc')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    story.append(level_table)
    story.append(Spacer(1, 30))

    # Детали проблем
    if report_data["issues"]:
        story.append(Paragraph("Детальный анализ проблем", heading_style))

        for i, group in enumerate(report_data["issues"], 1):
            # Заголовок группы
            group_title = f"{i}. {group['name']}"
            story.append(Paragraph(group_title, ParagraphStyle(
                'GroupTitle',
                parent=styles['Heading3'],
                fontSize=14,
                spaceBefore=15,
                spaceAfter=5,
                textColor=HexColor('#333333')
            )))

            # Информация о группе
            group_info = f"Критерий WCAG: {group['criterion']} | Уровень: {group['level']} | Количество: {group['count']}"
            story.append(Paragraph(group_info, normal_style))
            story.append(Spacer(1, 10))

            # Примеры проблем (до 3 для каждой группы)
            for j, issue in enumerate(group["issues"][:3], 1):
                issue_text = f"""
                <b>Пример {j}:</b><br/>
                <b>Элемент:</b> {_escape_html(issue['element'])}<br/>
                <b>Строка:</b> {issue['line']}<br/>
                <b>Описание:</b> {_escape_html(issue['message'])}<br/>
                <b>Рекомендация:</b> {_escape_html(issue['recommendation'])}
                """
                story.append(Paragraph(issue_text, normal_style))
                story.append(Spacer(1, 10))

            if len(group["issues"]) > 3:
                more_text = f"... и еще {len(group['issues']) - 3} проблем(а)"
                story.append(Paragraph(more_text, normal_style))

            story.append(Spacer(1, 15))
    else:
        story.append(Paragraph("Поздравляем! Проблемы доступности не найдены.",
                              ParagraphStyle('Success',
                                           parent=styles['Normal'],
                                           fontSize=16,
                                           alignment=1,
                                           textColor=HexColor('#00b894'))))

    # Сборка PDF
    doc.build(story)

    return pdf_path


def _get_level_summary(grouped_issues: list) -> dict:
    """Создает сводку по уровням критичности"""
    summary = {"A": 0, "AA": 0, "AAA": 0}
    for group in grouped_issues:
        level = group["level"]
        if level in summary:
            summary[level] += group["count"]
    return summary


def _format_timestamp(timestamp: str) -> str:
    """Форматирует временную метку для красивого отображения"""
    try:
        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        return dt.strftime("%d.%m.%Y %H:%M:%S")
    except:
        return timestamp


def _escape_html(text: str) -> str:
    """Экранирует HTML символы для безопасного отображения в PDF"""
    return (text.replace('&', '&amp;')
               .replace('<', '&lt;')
               .replace('>', '&gt;')
               .replace('"', '&quot;')
               .replace("'", '&#x27;'))
