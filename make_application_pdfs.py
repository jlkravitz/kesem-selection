# -*- coding: utf-8 -*-
import csv
import fpdf
import random

class PDF(fpdf.FPDF):
    def header(self):
        # Arial bold 15
        self.set_font('Arial', 'B', 15)
        # Calculate width of title and position
        w = self.get_string_width(title) + 6
        self.set_x((210 - w) / 2)
        # Colors of frame, background and text
        self.set_draw_color(0, 80, 180)
        self.set_fill_color(230, 230, 0)
        self.set_text_color(220, 50, 50)
        # Thickness of frame (1 mm)
        self.set_line_width(1)
        # Title
        self.cell(w, 9, title, 1, 1, 'C', 1)
        # Line break
        self.ln(10)

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Text color in gray
        self.set_text_color(128)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

    def chapter_title(self, num, label):
        # Arial 12
        self.set_font('Arial', '', 12)
        # Background color
        self.set_fill_color(200, 220, 255)
        # Title
        self.cell(0, 6, 'Chapter %d : %s' % (num, label), 0, 1, 'L', 1)
        # Line break
        self.ln(4)

    def chapter_body(self, name):
        # Read text file
        with open(name, 'rb') as fh:
            txt = fh.read().decode('latin-1')
        # Times 12
        self.set_font('Times', '', 12)
        # Output justified text
        self.multi_cell(0, 5, txt)
        # Line break
        self.ln()
        # Mention in italics
        self.set_font('', 'I')
        self.cell(0, 5, '(end of excerpt)')

    def print_chapter(self, num, title, name):
        self.add_page()
        self.chapter_title(num, title)
        self.chapter_body(name)

def add_question_to_pdf(pdf, q, a):
    a = a.replace('\x89\xdb\xd2', '--')
    a = a.replace('\x89\xdb\xaa', '\'')
    a = a.replace('\x89\xdb\xcf', '"')
    a = a.replace('\x89\xdb\x9d', '"')

    pdf.set_font('Arial', 'b', size=14)
    pdf.multi_cell(0, 10, txt=q, align='L')
    pdf.set_font('Arial', size=12)
    pdf.multi_cell(0, 10, txt=a, align='L')

def make_app_pdf(app, code):
    pdf = fpdf.FPDF(format='letter')
    # pdf.add_font('dejavu', '', 'fonts/DejaVuSansMono.ttf', uni=True)
    # pdf.add_font('dejavub', '', 'fonts/DejaVuSansMono-Bold.ttf', uni=True)
    pdf.add_page()
    pdf.set_font('Arial', size=22)
    pdf.cell(0, txt=str(code), ln=1, align='C')
    for q in app:
        add_question_to_pdf(pdf, q, str(app[q]))
    pdf.output('apps/{}.pdf'.format(str(code)))

def load_apps():
    with open('apps.csv', encoding='ISO-8859-1') as f:
        app_reader = csv.reader(f)
        headers = app_reader.__next__()
        apps = [app for app in app_reader] 
    return apps
def main():
    apps = load_apps()
    
    print(headers)
    # make_app_pdf(apps.next(), '123')
        # for app in apps:
            # These are applications that weren't submitted.
            # if app['Completion Status'] == '0':
                # continue
            # make_app_pdf(app, '123')

    # for idx, app in apps.iterrows():
    # make_app_pdf(apps[:1], 'Baby Blue')
        # print(app)


if __name__ == '__main__':
    main()

