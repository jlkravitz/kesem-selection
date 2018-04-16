from __future__ import print_function
import csv
import os
from wufoo_pdf import WufooPDF

def make_app_pdfs():
    apps = wufoo_entry_loader.load_apps(fields=['full_name', 'questions'])
    with open('camper_info.csv', 'r') as csvfile:
        camperreader = csv.reader(csvfile)
        headers = next(camperreader)
        for row in camperreader: 
            camper_name = row[0]
            pdf = WufooPDF()
            pdf.append(zip(headers[1:], row[1:]), camper_name)
            pdf.save(os.path.join('camper_files/', camper_name) + '.pdf')

def main():
    # os.mkdir('camper_files')
    make_app_pdfs()

if __name__ == '__main__':
    main()

