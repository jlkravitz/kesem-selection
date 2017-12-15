import csv
import fpdf
import os
import random
import re
from collections import OrderedDict
import wufoo_entry_loader

def add_title(pdf, title):
    pdf.set_font('dejavu', size=22)
    pdf.cell(0, txt=title, ln=1, align='C')
    pdf.cell(0, 10, ln=1)

def add_header(pdf, txt):
    pdf.set_font('dejavub', size=14)
    pdf.multi_cell(0, 10, txt=txt, align='L')

def add_paragraph(pdf, txt):
    pdf.set_font('dejavu', size=12)
    pdf.multi_cell(0, 10, txt=txt, align='L')

def add_spacing(pdf, height=10):
    pdf.cell(0, height, ln=1)

def preprocess_fpdf_text(text):
    # https://stackoverflow.com/questions/33404752/removing-emojis-from-a-string-in-python 
    # FPDF doesn't like emojis, so remove them here.
    emoji_pattern = re.compile('['
        u'\U0001F600-\U0001F64F'  # emoticons
        u'\U0001F300-\U0001F5FF'  # symbols & pictographs
        u'\U0001F680-\U0001F6FF'  # transport & map symbols
        u'\U0001F1E0-\U0001F1FF'  # flags (iOS)
       ']+', flags=re.UNICODE)
    text = emoji_pattern.sub(r'', text)

    # FPDF doesn't correctly display tabs. Just convert to spaces.
    text = text.replace('\t', '    ')

    return text

def add_question_to_pdf(pdf, question, answer):
    add_header(pdf, question)
    lines = [l for l in preprocess_fpdf_text(answer).splitlines() if l != '']
    for answer_line in lines:
        add_paragraph(pdf, answer_line)
        add_spacing(pdf, 4)

def make_app_pdf(app, title, directory):
    pdf = fpdf.FPDF(format='letter')
    pdf.add_font('dejavu', '', 'fonts/DejaVuSansCondensed.ttf', uni=True)
    pdf.add_font('dejavub', '', 'fonts/DejaVuSansCondensed-Bold.ttf', uni=True)
    pdf.add_page()
    add_title(pdf, title)
    for (i, (question, answer)) in enumerate(app):
        add_question_to_pdf(pdf, question, answer)
    pdf.output(os.path.join(directory, title + '.pdf'))

def load_applicant_ids():
    with open('applicant_ids.csv') as f:
        reader = csv.reader(f)
        return {
            app_id[0]: app_id[1]
            for app_id in reader
        }

def make_app_pdfs(applicant_ids):
    apps = wufoo_entry_loader.load_apps(fields=['full_name', 'questions'])
    for i, app in enumerate(apps):
        if i != 0 and i % 10 == 0:
            print('Made {}/{} Application PDFs'.format(i, len(apps)))
        make_app_pdf(app['questions'], 'Applicant #{}'.format(applicant_ids[app['full_name']]), 'apps')

def make_reference_pdfs(applicant_ids):
    references = wufoo_entry_loader.load_references(['applicant_full_name', 'questions'])
    for i, lor in enumerate(references):
        if i != 0 and i % 10 == 0:
            print('Made {}/{} Letter of Reference PDFs'.format(i, len(references)))

        # Applicant IDs come from the applications, so we don't have to try/catch
        # when looping over apps. Here, there may not exist an application for
        # the reference of the given name.
        try:
            title = 'Applicant #{}'.format(applicant_ids[lor['applicant_full_name']])
        except KeyError:
            print(('Letter of reference for "{}" has no corresponding application. Make sure to fix all ' +\
                  'issues listed by `cross_reference.py` before running this script.').format(lor['applicant_full_name']))
            continue

        make_app_pdf(lor['questions'], title, 'references')

def main():
    applicant_ids = load_applicant_ids()
    make_app_pdfs(applicant_ids)
    make_reference_pdfs(applicant_ids)

if __name__ == '__main__':
    main()

