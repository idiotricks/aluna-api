import csv
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch, mm
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, Spacer, PageBreak


class TOCSV:
    def __init__(self, header, data, response):
        self.header = header
        self.data = data
        self.response = response
        self.writer = csv.writer(self.response)

    def build(self):
        self.writer.writerow(self.header)
        for d in self.data:
            self.writer.writerow(d)
        return self.response


class TOPDF:
    def __init__(self, response, title, request):
        self.response = response
        self.request = request
        self.title = title
        self.elems = []
        self.date = datetime.now().strftime('%A, %d %B %Y %I:%M %p')
        self.pdf = None
        self.stylesheets = getSampleStyleSheet()

        self.set_pdf()

    def table_styles(self, single=False):
        if not single:
            return [
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
            ]

        return [
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ]

    def set_pdf(self):
        self.pdf = SimpleDocTemplate(
            self.response,
            title=self.title,
            pagesize=LETTER
        )

    def set_break(self, h=0.6, w=0.2):
        self.elems.append(Spacer(h, w * inch))

    def set_page_break(self):
        self.elems.append(PageBreak())

    def set_heading(self, title, level='title'):
        self.elems.append(Paragraph(title, style=self.stylesheets[level]))

    def set_heading_1(self, title):
        self.set_heading(title, 'h1')

    def set_heading_2(self, title):
        self.set_heading(title, 'h2')

    def set_heading_3(self, title):
        self.set_heading(title, 'h3')

    def set_heading_4(self, title):
        self.set_heading(title, 'h4')

    def set_text(self, text):
        self.elems.append(Paragraph(text, style=self.stylesheets['Normal']))

    def set_table(self, header, data, align, styles):
        if not styles:
            styles = self.table_styles()

        for i in range(1, len(data) + 1):
            if i % 2 == 0:
                bc = colors.lightgrey
            else:
                bc = colors.whitesmoke

            styles.append(('BACKGROUND', (0, i), (-1, i), bc))

        dataCopy = [header]
        for d in data:
            dataCopy.append(d)

        table = Table(dataCopy, hAlign=align)
        table.setStyle(styles)
        self.elems.append(table)

    def set_table_detail(self, data):
        styles = self.table_styles(single=True)

        table = Table(data, hAlign='LEFT')
        table.setStyle(styles)
        self.elems.append(table)

    def set_table_left(self, header, data, styles=None):
        self.set_table(header, data, 'LEFT', styles)

    def set_table_center(self, header, data, styles=None):
        self.set_table(header, data, 'CENTER', styles)

    def set_periode(self, request):
        periode = 'No Periode'
        if request.GET.get('start_date') and request.GET.get('end_date'):
            sd = request.GET.get('start_date')
            ed = request.GET.get('end_date')
            periode = f'{sd} s/d {ed}'

        return ['Periode', ':', periode]

    def set_user(self, request):
        user = 'No User'
        if request.user:
            user = request.user.username
        return ['Report by', ':', user]

    def set_date_created(self):
        return ['Created', ':', datetime.now().strftime('%d %B %Y %H:%M')]

    def set_subject(self, text):
        return ['Subject', ':', text]

    def set_other(self, key, value):
        return [key, ':', value]

    def build(self):
        self.pdf.build(self.elems)
        return self.response


class TOPDFBarcodeThermal(TOPDF):
    width = 110 * mm
    limit = 110 * mm

    def set_pdf(self):
        self.pdf = SimpleDocTemplate(
            self.response,
            title=self.title,
            rightMargin=0,
            leftMargin=0,
            topMargin=0,
            bottomMargin=0,
            pagesize=(self.width, self.limit)
        )
