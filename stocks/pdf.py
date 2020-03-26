from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph


def export_pdf_stock_in(data):
    pass


def print_pdf_stock_in(title, stock_in, response, item_ins):
    date = datetime.now().strftime('%A, %d %B %Y %I:%M %p')
    pdf = SimpleDocTemplate(
        response,
        title=title,
        pagesize=LETTER
    )
    elems = []
    stylesheets = getSampleStyleSheet()

    elems.append(Paragraph(
        f'Report {stock_in["numcode"]} <br></br>{date}',
        style=stylesheets['h1']
    ))

    elems.append(Spacer(0.6, 0.2 * inch))

    stock_in_data = [
        ['numcode', stock_in['numcode']],
        ['date', stock_in['date']],
        ['supplier', stock_in['supplier_name']],
        ['phone', stock_in['supplier_phone']],
    ]
    style_table_stock_in = [
        ('BACKGROUND', (0, 0), (0, -1), colors.blue),
        ('BACKGROUND', (1, 0), (1, -1), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ]
    table_stock_in = Table(stock_in_data, hAlign='LEFT')
    table_stock_in.setStyle(TableStyle(style_table_stock_in))
    elems.append(table_stock_in)

    elems.append(Spacer(0.6, 0.2 * inch))

    elems.append(Paragraph('Items', style=stylesheets['h3']))

    elems.append(Spacer(0.6, 0.2 * inch))

    style_table_item_in = [
        ('BACKGROUND', (0, 0), (-1, 0), colors.blue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ]

    for i in range(1, len(item_ins)):
        if i % 2 == 0:
            bc = colors.aliceblue
        else:
            bc = colors.fidlightblue

        style_table_item_in.append(('BACKGROUND', (0, i), (-1, i), bc))

    item_ins_data = [
        ['Product', 'Current Stock', 'Request Quantity', 'Current Stock Residual', ]
    ]

    total_request_stock = 0
    for item in item_ins:
        item_ins_data.append([
            item['product_name'],
            item['product_stock'],
            item['quantity'],
            item['residual_stock'],
        ])
        total_request_stock += item['quantity']

    table_item_in = Table(item_ins_data, hAlign='LEFT')
    table_item_in.setStyle(style_table_item_in)
    elems.append(table_item_in)

    elems.append(Spacer(4, 1 * inch))

    unit = 'unit'
    if total_request_stock > 0:
        unit = 'units'

    elems.append(Paragraph(
        f'** Total Request Stock: <br></br>{total_request_stock} {unit}',
        style=stylesheets['h2']
    ))

    pdf.build(elems)
