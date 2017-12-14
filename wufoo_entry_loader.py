import csv

def normalize(name):
    return ' '.join(name.strip().lower().split())

def make_name(first_name, last_name):
    return normalize(first_name) + ' ' + normalize(last_name)

def find_column_index(csv_header, column_name):
    return csv_header.index(column_name)  # Throw error if doesn't exist!

def load_wufoo_entries(csv_file_name, get_id_fn, fields={}):
    """Load apps CSV from exported Wufoo entries."""
    with open(csv_file_name) as f:
        entry_reader = csv.reader(f)
        header = next(entry_reader)  # header

        # We keep the most recent entry based on the identifier.
        entries = {}
        for row in entry_reader:
            entry = build_entry(row, fields)
            if row[-1] == '0':
                continue
            entries[get_id_fn(row)] = entry

        return entries.values()

def build_entry(row, fields):
    return {
        field_name: build_field_fn(row)
        for (field_name, build_field_fn) in fields.items()
    }

def load_apps(fields=['first_name', 'last_name', 'email']):
    APP_QUESTIONS = [
        ('Describe your relevant experience working with children.', 24),
        ('Describe your experience working at camp.', 25),
        ('Describe your leadership positions.', 26),
        ('Describe a favorite childhood memory.', 27),
        ('What are three things you want us to know about you?', 28),
        ('What is something you would be excited to teach or facilitate at camp?', 29),
        ('Why do you want to volunteer your time for Camp Kesem?', 30),
        ('In what ways would you contribute to the diversity of Kesem\'s community?', 31)
    ]
    fields_map = {
        'first_name': lambda row: normalize(row[1]),
        'last_name': lambda row: normalize(row[2]),
        'full_name': lambda row: make_name(row[1], row[2]),
        'email': lambda row: normalize(row[9]),
        'questions': lambda row: [(q, row[index]) for (q, index) in APP_QUESTIONS]
    }
    return load_wufoo_entries('apps.csv', fields_map['email'], fields=dict_subset(fields_map, fields))

def load_references(fields):
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
        'questions': lambda row: [(q, row[index]) for (q, index) in REFERENCE_QUESTIONS]
    }
    return load_wufoo_entries('references.csv', fields_map['reference_full_name'], fields=dict_subset(fields_map, fields))

def dict_subset(mapping, keys):
    return dict((k, mapping[k]) for k in keys)
