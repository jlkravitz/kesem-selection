import csv

def load_applicants():
    with open('applicant_ids.csv') as f:
        reader = csv.reader(f)
        return [row[0] for row in reader]

def main():
    applicants = load_applicants()
    
    with open('app_reading_conflicts_of_interest.csv', 'w') as f:
        writer = csv.writer(f)

        readers = []
        while True:
            reader = input('Enter application reader\'s name (or nothing to continue): ')
            if not reader:
                break
            readers.append(reader)

        writer.writerow([''] + readers)

        for applicant in applicants:
            writer.writerow([applicant])

    print()
    print('Wahoo! The CSV has been written to app_reading_violations.csv.')
    print('Open this file in a Google Sheet, have readers mark those apps they should not read, then run `assign_app_readers.py`')

if __name__ == '__main__':
    main()

