from __future__ import print_function
import csv
import fpdf
import os
import random
import re
import sys
from collections import OrderedDict
import wufoo_entry_loader
from wufoo_pdf import WufooPDF

def load_applicant_ids():
    with open(os.path.join('AppReading', 'applicant_ids.csv')) as f:
        reader = csv.reader(f)
        return {
            app_id[0]: app_id[1]
            for app_id in reader
        }

def make_app_pdfs(applicant_ids, anonymous):
    apps = wufoo_entry_loader.load_apps(fields=['full_name', 'questions'])
    for i, app in enumerate(apps):
        if i != 0 and i % 10 == 0:
            print('Made {}/{} Application PDFs'.format(i, len(apps)))

        app_name = app['full_name']
        app_id = applicant_ids[app_name]
        if anonymous:
            pdf_title = 'Applicant #{}'.format(app_id)
            file_name = app_id + '.pdf'
        else:
            pdf_title = '{} (#{})'.format(app_name, app_id)
            file_name = app_name + '.pdf'

        wufoo_pdf = WufooPDF()
        wufoo_pdf.append(app['questions'], pdf_title)
        wufoo_pdf.save(os.path.join('apps/', file_name))

def make_reference_pdfs(applicant_ids, anonymous):
    references = wufoo_entry_loader.load_references(['applicant_full_name', 'questions'])
    for i, reference in enumerate(references):
        if i != 0 and i % 10 == 0:
            print('Made {}/{} Letter of Reference PDFs'.format(i, len(references)))

        # Applicant IDs come from the applications, so we don't have to try/catch
        # when looping over apps. Here, there may not exist an application for
        # the reference of the given name.
        try:
            app_name = reference['applicant_full_name']
            app_id = applicant_ids[app_name]
        except KeyError:
            print(('Letter of reference for "{}" has no corresponding application. Make sure to fix all ' +\
                  'issues listed by `cross_reference.py` before running this script.').format(reference['applicant_full_name']))
            continue

        if anonymous:
            pdf_title = 'Reference for Applicant #{}'.format(app_id)
            file_name = app_id + '.pdf'
        else:
            pdf_title = 'Reference for {} (#{})'.format(app_name, app_id)
            file_name = app_name + '.pdf'

        wufoo_pdf = WufooPDF()
        wufoo_pdf.append(reference['questions'], pdf_title)
        wufoo_pdf.save(os.path.join('references/', file_name))

def main():
    anonymous = raw_input('Would you like application PDFs to be anonymous (Y or N)? ')
    anonymous = anonymous.strip().lower() == 'y'
    os.mkdir('apps')
    os.mkdir('references')
    applicant_ids = load_applicant_ids()
    make_app_pdfs(applicant_ids, anonymous)
    make_reference_pdfs(applicant_ids, anonymous)

if __name__ == '__main__':
    main()

