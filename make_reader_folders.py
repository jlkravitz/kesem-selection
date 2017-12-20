from __future__ import print_function
from collections import defaultdict
import csv
import random
import os
import app_reader_folder

READERS_PER_APPLICANT = 2

def load_conflicts_of_interest():
    with open(os.path.join('AppReading', 'conflicts_of_interest.csv')) as f:
        conflicts_reader = csv.reader(f)
        reader_conflicts = dict((r, set()) for r in next(conflicts_reader)[1:])
        for row in conflicts_reader:
            applicant = row[0]
            for (reader, conflict_cell) in zip(reader_conflicts.keys(), row[1:]):
                if conflict_cell:
                    reader_conflicts[reader].add(applicant)

    return reader_conflicts

def load_applicants():
    with open(os.path.join('AppReading', 'applicant_ids.csv')) as f:
        reader = csv.reader(f)
        return dict((row[0], row[1]) for row in reader)  # name --> id

def make_app_assignments(name2id, conflicts_of_interest):

    def count_conflicts(applicant):
        return -sum(applicant[0] in conflicts
                for conflicts in conflicts_of_interest.values())

    app2readers = defaultdict(list)
    reader2apps = defaultdict(list)

    readers = list(conflicts_of_interest.keys())

    # Why do we sort by number of conflicts? Honestly, I'm not sure if it's a
    # heuristic that I educationally-guessed would work well or if it
    # mathematically works. It's easier to think about what would go wrong if
    # we didn't do this.
    #
    # Suppose we have 2 applicants and 2 readers and 1 reader/app.  Reader 1
    # has no conflicts. Reader 2 cannot read Applicant 2's app. Consider the
    # case where we assign Reader 1 to read Applicant 1. Next, we look at
    # Applicant 2 and see that only Reader 1 can read that app, so we assign it
    # to Reader 1, also. But now Reader 1 is reading 2 apps and Reader 2 is
    # reading none! Basically, this can cause imbalance.
    #
    # By sorting the list, we would first assign Reader 1 to Applicant 2.
    # Then, we would consider Applicant 1, which could be assigned to Reader 2.
    #
    # NOTE: the way the current algorithm is implemented, it's not *guaranteed*
    # that Reader 2 would be assigned to Applicant 1. We randomize the readers
    # for each iteration so it tends to work out.
    applicants = sorted(list(name2id.items()), key=count_conflicts)

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

        # Randomizing readers avoids the scenario where the same pairs of readers
        # are assigned to applicants.
        random.shuffle(readers)
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
    with open(os.path.join('AppReading', 'app_read_assignments.csv'), 'w') as f:
        writer = csv.writer(f)
        readers = list(reader2apps.keys())
        writer.writerow([''] + readers)
        for (applicant, app_readers) in app2readers.items():
            (name, id_) = applicant
            writer.writerow([name] + [('x' if reader in app_readers else '') for reader in readers])

def load_app_assignments(applicants):
    reader2apps = defaultdict(list)
    with open(os.path.join('AppReading', 'app_read_assignments.csv')) as f:
        csv_reader = csv.reader(f)
        readers = list(next(csv_reader))[1:]
        for row in csv_reader:
            name = row[0]
            id_ = applicants[name]
            app_readers = [readers[i] for i, val in enumerate(row[1:]) if val != '']
            for reader in app_readers:
                reader2apps[reader].append((name, id_))
    return reader2apps

def make_reader_folders(reader2apps):
    for (reader, applicants) in reader2apps.items():
        random.shuffle(applicants)
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
    raw_input()
    make_reader_folders(reader2apps)

if __name__ == '__main__':
    main()

