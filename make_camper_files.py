from __future__ import print_function
import csv
import os
from wufoo_pdf import WufooPDF

def make_app_pdfs():
    with open('camper_info.csv', 'r') as csvfile:
        camperreader = csv.reader(csvfile)
        headers = next(camperreader)
        for row in camperreader: 
            camper_name = row[0]
            pdf = WufooPDF()
            pdf.append(zip(headers[1:], row[1:]), camper_name)
            unit_dir = os.path.join('camper_files/', row[1])
            if not os.path.isdir(unit_dir):
                os.mkdir(unit_dir)
            pdf.save(os.path.join(unit_dir, camper_name) + '.pdf')

def main():
    if not os.path.isdir('camper_files'):
        os.mkdir('camper_files')
    make_app_pdfs()

if __name__ == '__main__':
    main()

