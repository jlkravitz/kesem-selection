import csv
import fpdf
import os
import random
import re
from collections import OrderedDict
import wufoo_entry_loader
from wufoo_pdf import WufooPDF

def load_applicant_ids():
    with open('applicant_ids.csv') as f:
        reader = csv.reader(f)
        return {
            app_id[0]: app_id[1]
            for app_id in reader
        }

def make_app_pdfs(applicant_ids):
    os.mkdir('apps')
    apps = wufoo_entry_loader.load_apps(fields=['full_name', 'questions'])
    for i, app in enumerate(apps):
        if i != 0 and i % 10 == 0:
            print('Made {}/{} Application PDFs'.format(i, len(apps)))
        wufoo_pdf = WufooPDF()
        title = 'Applicant #{}'.format(applicant_ids[app['full_name']])
        wufoo_pdf.append(app['questions'], title)
        wufoo_pdf.save('apps/', title)

def make_reference_pdfs(applicant_ids):
    os.mkdir('references')
    references = wufoo_entry_loader.load_references(['applicant_full_name', 'questions'])
    for i, reference in enumerate(references):
        if i != 0 and i % 10 == 0:
            print('Made {}/{} Letter of Reference PDFs'.format(i, len(references)))

        # Applicant IDs come from the applications, so we don't have to try/catch
        # when looping over apps. Here, there may not exist an application for
        # the reference of the given name.
        try:
            title = 'Reference for Applicant #{}'.format(applicant_ids[reference['applicant_full_name']])
        except KeyError:
            print(('Letter of reference for "{}" has no corresponding application. Make sure to fix all ' +\
                  'issues listed by `cross_reference.py` before running this script.').format(reference['applicant_full_name']))
            continue

        wufoo_pdf = WufooPDF()
        wufoo_pdf.append(reference['questions'], title)
        wufoo_pdf.save('references/', title)

def main():
    applicant_ids = load_applicant_ids()
    make_app_pdfs(applicant_ids)
    make_reference_pdfs(applicant_ids)

if __name__ == '__main__':
    main()

