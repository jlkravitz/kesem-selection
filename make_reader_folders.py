from collections import defaultdict
import csv
import random
import os
import app_reader_folder

READERS_PER_APPLICANT = 2

def load_conflicts_of_interest():
    with open('conflicts_of_interest.csv') as f:
        conflicts_reader = csv.reader(f)
        reader_conflicts = dict((r, set()) for r in next(conflicts_reader)[1:])
        for row in conflicts_reader:
            applicant = row[0]
            for (reader, conflict_cell) in zip(reader_conflicts.keys(), row[1:]):
                if conflict_cell:
                    reader_conflicts[reader].add(applicant)

    return reader_conflicts

def load_applicants():
    with open('applicant_ids.csv') as f:
        reader = csv.reader(f)
        return dict((row[0], row[1]) for row in reader)  # name --> id

def make_app_assignments(name2id, conflicts_of_interest):
    app2readers = defaultdict(list)
    reader2apps = defaultdict(list)

    readers = list(conflicts_of_interest.keys())
    random.shuffle(readers)

    applicants = list(name2id.items())
    random.shuffle(applicants)

    # This continues assigning readers to applicants until no A single
    # iteration iterates through all reader/applicant pairs and tries to assign
    # them if possible. If a single iteration yields no changes in the
    # assignment, we have done all we can do.
    # 
    # NOTE: This is a greedy algorithm so has the potential to fail in some
    # cases. I would guess that that won't be too common, though, unless a few
    # of the readers are *very* popular and aren't able to read many apps.
    prev_assigned = -1
    curr_assigned = 0
    while curr_assigned > prev_assigned:
        prev_assigned = curr_assigned
        for reader in readers:
            for (name, id_) in applicants:
                if name not in conflicts_of_interest[reader] and \
                        (name, id_) not in reader2apps[reader] and \
                        len(app2readers[(name, id_)]) < READERS_PER_APPLICANT:
                    curr_assigned += 1
                    app2readers[(name, id_)].append(reader)
                    reader2apps[reader].append((name, id_))
                    break

    return reader2apps, app2readers

def save_app_assignments(reader2apps, app2readers):
    with open('app_read_assignments.csv', 'w') as f:
        writer = csv.writer(f)
        readers = list(reader2apps.keys())
        writer.writerow([''] + readers)
        for (applicant, app_readers) in app2readers.items():
            (name, id_) = applicant
            writer.writerow([name] + [('x' if reader in app_readers else '') for reader in readers])

def make_reader_folders(reader2apps):
    for (reader, applicants) in reader2apps.items():
        folder = app_reader_folder.AppReaderFolder(reader, applicants)
        folder.make_score_sheet()
        folder.make_app_packet()

def main():
    conflicts_of_interest = load_conflicts_of_interest()
    applicants = load_applicants()
    reader2apps, app2readers = make_app_assignments(applicants, conflicts_of_interest)
    save_app_assignments(reader2apps, app2readers)
    print('Quickly inspect app assignments in app_read_assignments.csv to make sure ' +\
            'nothing looks fishy (enter to continue)...')
    input()
    make_reader_folders(reader2apps)

if __name__ == '__main__':
    main()

