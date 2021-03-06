from __future__ import print_function
import csv
import os

def load_applicants():
    with open(os.path.join('AppReading', 'applicant_ids.csv')) as f:
        reader = csv.reader(f)
        return [row[0] for row in reader]

def main():
    applicants = load_applicants()
    
    with open(os.path.join('AppReading', 'conflicts_of_interest.csv'), 'w') as f:
        writer = csv.writer(f)

        readers = []
        while True:
            reader = raw_input('Enter application reader\'s name (or nothing to continue): ')
            if not reader:
                break
            readers.append(reader)

        writer.writerow([''] + readers)

        for applicant in applicants:
            writer.writerow([applicant])

    print()
    print('Wahoo! The CSV has been written to conflicts_of_interest.csv.')
    print('Open this file in a Google Sheet, have readers mark those apps they should not read, then run `assign_app_readers.py`')

if __name__ == '__main__':
    main()

