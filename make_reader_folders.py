from collections import defaultdict
import csv
import os
from wufoo_pdf import WufooPDF
import wufoo_entry_loader

READERS_PER_APPLICANT = 2

def load_conflicts_of_interest():
    with open('app_reading_conflicts_of_interest.csv') as f:
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
    assigned = defaultdict(int) # dictionary from ids to # readers
    assignments = defaultdict(dict)  # dictionary from reader to applicant ids

    while len(assigned) < len(applicants) or not all(n >= READERS_PER_APPLICANT for n in assigned.values()):
        for reader in conflicts_of_interest:
            for (name, id_) in applicants.items():
                if name not in conflicts_of_interest[reader] and \
                        assigned[id_] < READERS_PER_APPLICANT:
                    assigned[id_] += 1
                    assignments[reader][name] = id_
                    break

    return assignments

def make_score_sheet(applicants, reader, save_dir):
    with open(os.path.join(save_dir, reader + ' Score Sheet.csv'), 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['', 'Score (1-5)', 'Notes'])
        for id_ in applicants.values():
            writer.writerow([id_])

def make_app_packet(applicants, reader, save_dir):

    def get_questions(name, entries):
        for entry in entries:
            if entry['full_name'] == name:
                return entry['questions']
        raise KeyError

    packet = WufooPDF()
    packet.add_cover_page(reader + '\'s Application Packet')

    apps = wufoo_entry_loader.load_apps(fields=['full_name', 'questions'])
    references = wufoo_entry_loader.load_references(fields=['applicant_full_name', 'questions'], rename={'applicant_full_name': 'full_name'})

    for (name, id_) in applicants.items():
        app_questions = get_questions(name, apps)
        packet.append(app_questions[:-2], 'Applicant #{}'.format(id_))
        packet.add_cover_page('STOP!\nGive a pre-special sauce score before looking at Special Sauce.')
        packet.append(app_questions[-2:])
        packet.add_cover_page('STOP!\nGive a post-special sauce score before reading the letter of reference.')

        try:
            reference_questions = get_questions(name, references)
            packet.append(reference_questions, 'Reference for Applicant #{}'.format(id_))
            packet.add_cover_page('STOP!\nGive a post-reference score before continuing on to the next application.')
        except KeyError:
            packet.add_cover_page('Reference for Applicant #{} is missing.'.format(id_))

    packet.save(os.path.join(save_dir, reader + ' Application Packet.pdf'))

def make_reader_folders(assignments, applicants):
    root_dir = 'Application Reads'
    os.mkdir(root_dir)
    for (reader, applicants) in assignments.items():
        reader_dir = os.path.join(root_dir, reader)
        os.mkdir(reader_dir)
        make_score_sheet(applicants, reader, reader_dir)
        make_app_packet(applicants, reader, reader_dir)

def main():
    conflicts_of_interest = load_conflicts_of_interest()
    applicants = load_applicants()
    assignments = make_app_assignments(applicants, conflicts_of_interest)
    make_reader_folders(assignments, applicants)

if __name__ == '__main__':
    main()

