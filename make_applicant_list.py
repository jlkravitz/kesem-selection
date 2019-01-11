from __future__ import print_function
import csv
import os
import wufoo_entry_loader

def load_applicant_ids():
    with open(os.path.join('AppReading', 'applicant_ids.csv')) as f:
        reader = csv.reader(f)
        return {
            app_id[0]: app_id[1]
            for app_id in reader
        }

def main():
    applicant_ids = load_applicant_ids()
    apps = wufoo_entry_loader.load_apps(fields=['full_name', 'school_year', 'gender'])

    with open(os.path.join('AppReading', 'applicant_list.csv'), 'w') as f:
        writer = csv.writer(f)

        for app in apps:
            writer.writerow([applicant_ids[app['full_name']], app['full_name'], app['school_year'], app['gender']])

if __name__ == '__main__':
    main()

