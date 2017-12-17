"""Helper library for loading Wufoo form entries into python.

Some general terms and abstractions used in this file...
    • column: original column name in the CSV file full of Wufoo entries
    • field: value derived from original columns meant for python objects
             representing Wufoo entries
    • entry: refers to both Wufoo entries (form submissions) and python
             entries (pythonic representations of these submissions)
 """

import csv

def normalize(name):
    return ' '.join(name.strip().lower().split())

def make_name(first_name, last_name):
    return normalize(first_name) + ' ' + normalize(last_name)

def load_wufoo_entries(csv_file_name, key,
        field_map, fields, rename):
    """Load apps CSV from exported Wufoo entries.

    Parameters
    ----------
    csv_file_name: str
        the name of the csv file containing Wufoo form entries
    key: fn(row) --> str
        the name of the column in the csv file which identifies a particular
        Wufoo entry
        this is usually a name or email
    field_map: dict(str, fn)
        maps fields to their corresponding builder functions, which build the
        field from the original columns of the Wufoo entries
    fields: list(str)
        the fields requested – all fields in this list should be keys of `field_map`
    rename: dict(str, str)
        maps fields to new names

    """
    with open(csv_file_name) as f:
        entry_reader = csv.reader(f)
        header = next(entry_reader)  # header

        # We keep the most recent entry based on the identifier.
        return [
            build_entry(row, field_map, fields, rename)
            for row in entry_reader
            if row[-1] == '1'  # Checks if Wufoo entry was actually submitted]
        ]

def build_entry(row, field_map, fields, rename):
    return {
        rename.get(field_name, field_name): field_map[field_name](row)
        for field_name in fields
    }

def load_apps(fields, rename={}):
    APP_QUESTIONS = [
        ('Describe your relevant experience working with children.', 24),
        ('Describe your experience working at camp.', 25),
        ('Describe your leadership positions.', 26),
        ('Describe a favorite childhood memory.', 27),
        ('What are three things you want us to know about you?', 28),
        ('What is something you would be excited to teach or facilitate at camp?', 29),
        ('Why do you want to volunteer your time for Camp Kesem?', 30),
        ('In what ways would you contribute to the diversity of Kesem\'s community?', 31),
        ('Special Sauce', 32),
        ('Additional Info', 33),
        ('Additional Info Upload (sometimes contains special sauce)', 34)
    ]
    fields_map = {
        'first_name': lambda row: normalize(row[1]),
        'last_name': lambda row: normalize(row[2]),
        'full_name': lambda row: make_name(row[1], row[2]),
        'email': lambda row: normalize(row[9]),
        'school_year': lambda row: row[7],
        'gender': lambda row: normalize(row[5]),
        'submission_time': lambda row: row[37],
        'questions': lambda row: [(q, row[index]) for (q, index) in APP_QUESTIONS]
    }
    key = fields_map['email']
    return load_wufoo_entries('apps.csv', key, fields_map, fields, rename )

def load_references(fields, rename={}):
    REFERENCE_QUESTIONS = [
        ('How do they know the applicant?', 7),
        ('How well does the applicant work with others in a team environment?', 8),
        ('Elaborate', 9),
        ('How well does they communicate with peers?', 10),
        ('Elaborate', 11),
        ('How well do they manage stressful situations?', 12),
        ('Elaborate', 13),
        ('To what extent are they willing to take initiative?', 14),
        ('Elaborate', 15),
        ('How good of a listener are they?', 16),
        ('Elaborate', 17),
        ('How well can you imagine the applicant engaging with campers?', 18),
        ('Elaborate', 19),
        ('How would you rank their energy level?', 20),
        ('Any reservations?', 21),
        ('Anything else?', 22)
    ]
    fields_map = {
        'reference_first_name': lambda row: normalize(row[1]),
        'reference_last_name': lambda row: normalize(row[2]),
        'reference_full_name': lambda row: make_name(row[1], row[2]),
        'applicant_first_name': lambda row: normalize(row[5]),
        'applicant_last_name': lambda row: normalize(row[6]),
        'applicant_full_name': lambda row: make_name(row[5], row[6]),
        'submission_time': lambda row: row[26],
        'questions': lambda row: [(q, row[index]) for (q, index) in REFERENCE_QUESTIONS]
    }
    key = lambda row: (fields_map['reference_full_name'](row), fields_map['applicant_full_name'](row))
    return load_wufoo_entries('references.csv', key, fields_map, fields, rename)

