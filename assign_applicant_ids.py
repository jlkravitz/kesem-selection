"""This script writes out a CSV file mapping applicant names to applicant IDs.

Note: The order is randomized each time, so only run this once!
"""
import csv
import random

COMPLETION_STATUS_COL = -1

def preprocess_name(name):
    return ' '.join(name.strip().lower().split())

def make_name(first_name, last_name):
    return '{} {}'.format(first_name, last_name)

def save_applicant_ids(apps):
    with open('applicant_ids.csv', 'w') as f:  #utf-8
        writer = csv.writer(f)
        for i, app in enumerate(apps):
            writer.writerow([app['name'], str(i)])

def load_apps():
    """Load apps CSV from exported Wufoo entries."""
    with open('apps.csv') as f:  #ISO-8859-1
        return [
            {
                'name': preprocess_name(make_name(app[1], app[2]))
            }
            for app in csv.reader(f)
            if app[COMPLETION_STATUS_COL] == '1'  # This implicitly skips the header row
        ]

def main():
    apps = load_apps()
    random.shuffle(apps)
    save_applicant_ids(apps)

if __name__ == '__main__':
    main()
