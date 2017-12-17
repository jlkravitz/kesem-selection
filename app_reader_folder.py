import csv
import os
import wufoo_pdf
import wufoo_entry_loader

class AppReaderFolder(object):
    def __init__(self, reader, assigned_applicants):
        self.reader = reader

        self.reader_dir = os.path.join('Application Reads', reader)
        if not os.path.exists(self.reader_dir):
            os.makedirs(self.reader_dir)

        self.assigned_applicants = assigned_applicants  # dict from name to id

    def make_score_sheet(self):
        with open(os.path.join(self.reader_dir, self.reader + ' Score Sheet.csv'), 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['', 'Score (1-5)', 'Notes'])
            for id_ in self.assigned_applicants.values():
                writer.writerow([id_])

    def make_app_packet(self):

        def get_questions(name, entries):
            for entry in entries:
                if entry['full_name'] == name:
                    return entry['questions']
            raise KeyError

        packet = wufoo_pdf.WufooPDF()
        packet.add_cover_page(self.reader + '\'s Application Packet')

        apps = wufoo_entry_loader.load_apps(fields=['full_name', 'questions'])
        references = wufoo_entry_loader.load_references(fields=['applicant_full_name', 'questions'], rename={'applicant_full_name': 'full_name'})

        for (name, id_) in self.assigned_applicants.items():
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

        packet.save(os.path.join(self.reader_dir, self.reader + ' Application Packet.pdf'))

