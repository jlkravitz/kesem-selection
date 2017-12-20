from __future__ import print_function
import csv
import os
import app_reader_folder

def load_applicant_id2name():
    with open('applicant_ids.csv') as f:
        reader = csv.reader(f)
        return dict((row[1], row[0]) for row in reader)

def redo_reader_packets():
    id2name = load_applicant_id2name()
    readers = next(os.walk('Application Reading'))[1]
    for reader in readers:
        with open('Application Reading/{}/{} Score Sheet.csv'.format(reader, reader)) as f:
            csv_reader = csv.reader(f)
            next(csv_reader)
            reader_apps = []
            for row in csv_reader:
                id_ = row[0]
                reader_apps.append((id2name[id_], id_))

        app_reader_folder.AppReaderFolder(reader, reader_apps).make_app_packet()

def main():
    redo_reader_packets()

if __name__ == '__main__':
    main()

