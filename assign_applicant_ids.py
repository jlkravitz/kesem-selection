"""This script writes out a CSV file mapping applicant names to applicant IDs.

Note: The order is randomized each time, so only run this once!
"""
import csv
import random
import wufoo_entry_loader

def main():
    apps = wufoo_entry_loader.load_apps(['name'])
    random.shuffle(apps)

    # Save applicant IDs.
    # Index in list is their ID.
    with open('applicant_ids.csv', 'w') as f:
        writer = csv.writer(f)
        for i, app in enumerate(apps):
            writer.writerow([app['name'], str(i)])

if __name__ == '__main__':
    main()

