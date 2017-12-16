from collections import defaultdict
import csv
import os
import make_pdfs

READERS_PER_APPLICANT = 2

def load_assignment_violations():
    violations = defaultdict(set)
    with open('app_reading_violations.csv') as f:
        violations_reader = csv.reader(f)
        readers = next(violations_reader)[1:]
        for row in violations_reader:
            applicant = row[0]
            for (reader, violation_cell) in zip(readers, row[1:]):
                if violation_cell:
                    violations[reader].add(applicant)

    return violations  # SORT BY VIOLATION #?

def load_applicants():
    with open('applicant_ids.csv') as f:
        reader = csv.reader(f)
        return dict((row[0], row[1]) for row in reader)  # name --> id

def main():
    assignment_violations = load_assignment_violations()
    applicants = load_applicants()

    assigned = defaultdict(int) # dictionary from ids to # readers
    assignments = defaultdict(list)  # dictionary from reader to applicant ids

    while len(assigned) < len(applicants) or not all(n >= READERS_PER_APPLICANT for n in assigned.values()):
        for reader in assignment_violations:
            for (name, id_) in applicants.items():
                if name not in assignment_violations[reader] and \
                        assigned[id_] < READERS_PER_APPLICANT:
                    assigned[id_] += 1
                    assignments[reader].append(id_)
                    break
 
    root_dir = 'Application Reads'
    os.mkdir(root_dir)
    for (reader, applicants) in assignments.items():
        reader_dir = os.path.join(root_dir, reader)
        os.mkdir(reader_dir)
        with open(os.path.join(reader_dir, 'Score Sheet.csv'), 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['', 'Score (1-5)', 'Notes'])
            for applicant in applicants:
                writer.writerow([applicant])
        make_pdfs.make_app_packet(applicants, reader)

if __name__ == '__main__':
    main()

