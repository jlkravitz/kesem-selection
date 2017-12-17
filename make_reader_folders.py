from collections import defaultdict
import csv
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
                    conflicts[reader].add(applicant)

    return reader_conflicts

def load_applicants():
    with open('applicant_ids.csv') as f:
        reader = csv.reader(f)
        return dict((row[0], row[1]) for row in reader)  # name --> id

def make_app_assignments(applicants, conflicts_of_interest):
    id2readers = dict((id_, []) for id_ in applicants.values())
    reader2ids = defaultdict(dict)  # reader --> applicant name --> applicant id

    # NOTE: This will fail in some cases if assignments aren't possible.
    prev_assigned = -1
    curr_assigned = 0
    while curr_assigned > prev_assigned:
        prev_assigned = curr_assigned
        for reader in conflicts_of_interest:
            for (name, id_) in applicants.items():
                if name not in conflicts_of_interest[reader] and \
                        len(id2readers[id_]) < READERS_PER_APPLICANT:
                    curr_assigned += 1
                    id2readers[id_].append(reader)
                    reader2ids[reader][name] = id_
                    break

    return reader2ids

def make_reader_folders(assignments):
    for (reader, applicants) in assignments.items():
        folder = app_reader_folder.AppReaderFolder(reader, applicants)
        folder.make_score_sheet()
        folder.make_app_packet()

def main():
    conflicts_of_interest = load_conflicts_of_interest()
    applicants = load_applicants()
    assignments = make_app_assignments(applicants, conflicts_of_interest)
    make_reader_folders(assignments)

if __name__ == '__main__':
    main()

